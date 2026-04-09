"""
AlphaFold DB Integration Service
Fetches protein structures from AlphaFold Database with confidence scores.
Integrates sequence search via UniProt API.
"""

import requests
import re
import logging
from pathlib import Path
from typing import Optional, Dict, Tuple
import time

logger = logging.getLogger(__name__)

class AlphaFoldService:
    """Service to fetch AlphaFold predictions and confidence scores."""
    
    # API endpoints
    UNIPROT_API = "https://rest.uniprot.org/uniprotkb/search"
    ALPHAFOLD_API = "https://alphafold.ebi.ac.uk/api/prediction"
    ALPHAFOLD_DOWNLOAD = "https://alphafold.ebi.ac.uk/files"
    
    # Rate limiting (AlphaFold DB is generous, but let's be respectful)
    REQUEST_DELAY = 0.2  # seconds between requests
    TIMEOUT = 10  # seconds
    
    def __init__(self):
        """Initialize AlphaFold service."""
        self.session = requests.Session()
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Respect rate limits between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.REQUEST_DELAY:
            time.sleep(self.REQUEST_DELAY - elapsed)
        self.last_request_time = time.time()
    
    def search_sequence_in_uniprot(self, sequence: str) -> Optional[Dict]:
        """
        Search for a sequence in UniProt database.
        Returns UniProt entry with ID and metadata.
        """
        try:
            # Clean sequence
            seq_clean = sequence.strip().upper()
            seq_clean = ''.join([c for c in seq_clean if c.isalpha()])
            
            if len(seq_clean) < 10:
                logger.warning(f"Sequence too short ({len(seq_clean)} AA)")
                return None
            
            # Use UniProt search API for exact sequence match
            query = f"sequence:{seq_clean}"
            params = {
                'query': query,
                'format': 'json',
                'size': 1,  # Just get the best match
                'fields': 'accession,id,protein_name,organism_name,sequence'
            }
            
            logger.info(f"Searching UniProt for sequence ({len(seq_clean)} AA)...")
            self._rate_limit()
            
            response = self.session.get(
                self.UNIPROT_API,
                params=params,
                timeout=self.TIMEOUT,
                headers={'User-Agent': 'CESGA-AlphaFold-Integration'}
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            if not results:
                logger.info(f"No UniProt match found for sequence")
                return None
            
            entry = results[0]
            uniprot_id = entry.get('primaryAccession', '')
            
            logger.info(f"✅ Found UniProt match: {uniprot_id}")
            
            return {
                'uniprot_id': uniprot_id,
                'entry_id': entry.get('uniProtkbId', ''),
                'protein_name': entry.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'Unknown'),
                'organism': entry.get('organism', {}).get('scientificName', 'Unknown'),
                'sequence': entry.get('sequence', {}).get('value', ''),
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"UniProt search error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error searching UniProt: {e}")
            return None
    
    def get_alphafold_structure(self, uniprot_id: str) -> Optional[Dict]:
        """
        Fetch AlphaFold prediction for a UniProt ID.
        Returns PDB structure with confidence scores (pLDDT).
        """
        try:
            if not uniprot_id:
                return None
            
            logger.info(f"Querying AlphaFold DB for {uniprot_id}...")
            self._rate_limit()
            
            # Query AlphaFold API
            response = self.session.get(
                f"{self.ALPHAFOLD_API}/{uniprot_id}",
                timeout=self.TIMEOUT,
                headers={'User-Agent': 'CESGA-AlphaFold-Integration'}
            )
            
            if response.status_code == 404:
                logger.warning(f"No AlphaFold prediction found for {uniprot_id}")
                return None
            
            response.raise_for_status()
            
            predictions = response.json()
            if not predictions:
                logger.warning(f"Empty response for {uniprot_id}")
                return None
            
            # Get the first (best) prediction
            prediction = predictions[0]
            
            # Extract relevant URLs and metadata
            result = {
                'uniprot_id': prediction.get('uniprotId', uniprot_id),
                'pdb_url': prediction.get('pdbUrl', ''),
                'cif_url': prediction.get('cifUrl', ''),
                'pae_image_url': prediction.get('paeImageUrl', ''),
                'pae_url': prediction.get('paeUrl', ''),
                'model_title': prediction.get('modelTitle', ''),
                'model_type': prediction.get('modelType', 'AF2-monomer'),
                'version': prediction.get('version', 1),
            }
            
            # Download PDB file and parse pLDDT
            if result['pdb_url']:
                pdb_data = self._download_pdb(result['pdb_url'])
                if pdb_data:
                    result['pdb_content'] = pdb_data['pdb_content']
                    result['plddt_scores'] = pdb_data['plddt_scores']
                    result['avg_plddt'] = pdb_data['avg_plddt']
                    logger.info(f"✅ Downloaded AlphaFold PDB for {uniprot_id} (avg pLDDT: {result['avg_plddt']:.1f})")
                else:
                    logger.warning(f"Failed to download PDB for {uniprot_id}")
                    return None
            else:
                logger.warning(f"No PDB URL in response for {uniprot_id}")
                return None
            
            return result
        
        except requests.exceptions.RequestException as e:
            logger.error(f"AlphaFold API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching AlphaFold structure: {e}")
            return None
    
    def _download_pdb(self, pdb_url: str) -> Optional[Dict]:
        """
        Download PDB file and extract pLDDT confidence scores.
        pLDDT values are stored in the B-factor column in AlphaFold PDBs.
        """
        try:
            self._rate_limit()
            
            response = self.session.get(
                pdb_url,
                timeout=self.TIMEOUT,
                headers={'User-Agent': 'CESGA-AlphaFold-Integration'}
            )
            response.raise_for_status()
            
            pdb_content = response.text
            
            # Parse pLDDT scores from B-factor column
            plddt_scores = []
            lines = pdb_content.split('\n')
            
            for line in lines:
                if line.startswith('ATOM'):
                    try:
                        # PDB format: pLDDT is at position 61-66 (6 chars) in ATOM records
                        # (in the B-factor column)
                        b_factor = line[61:66].strip()
                        if b_factor:
                            plddt = float(b_factor)
                            plddt_scores.append(plddt)
                    except (ValueError, IndexError):
                        continue
            
            # Calculate average pLDDT
            avg_plddt = sum(plddt_scores) / len(plddt_scores) if plddt_scores else 0.0
            
            # Categorize confidence
            if avg_plddt >= 90:
                confidence = "Very high"
            elif avg_plddt >= 70:
                confidence = "High"
            elif avg_plddt >= 50:
                confidence = "Medium"
            else:
                confidence = "Low"
            
            return {
                'pdb_content': pdb_content,
                'plddt_scores': plddt_scores,
                'avg_plddt': avg_plddt,
                'confidence': confidence,
                'num_atoms': len(plddt_scores),
            }
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download PDB: {e}")
            return None
        except Exception as e:
            logger.error(f"Error parsing PDB: {e}")
            return None
    
    def predict_structure_from_sequence(self, sequence: str) -> Optional[Dict]:
        """
        Complete pipeline: Sequence → UniProt search → AlphaFold prediction.
        Returns full structure with confidence metrics.
        """
        logger.info("Starting AlphaFold prediction pipeline...")
        
        # Step 1: Search UniProt
        uniprot_match = self.search_sequence_in_uniprot(sequence)
        if not uniprot_match:
            logger.warning("Sequence not found in UniProt, cannot use AlphaFold DB")
            return None
        
        uniprot_id = uniprot_match['uniprot_id']
        logger.info(f"Identified as: {uniprot_match['protein_name']} ({uniprot_id})")
        
        # Step 2: Fetch from AlphaFold
        alphafold_result = self.get_alphafold_structure(uniprot_id)
        if not alphafold_result:
            logger.warning(f"No AlphaFold prediction for {uniprot_id}")
            return None
        
        # Combine results
        result = {**uniprot_match, **alphafold_result}
        result['source'] = 'AlphaFold DB'
        result['pipeline_success'] = True
        
        return result


# Singleton instance
_alphafold_service = None

def get_alphafold_service() -> AlphaFoldService:
    """Get or create AlphaFold service singleton."""
    global _alphafold_service
    if _alphafold_service is None:
        _alphafold_service = AlphaFoldService()
    return _alphafold_service
