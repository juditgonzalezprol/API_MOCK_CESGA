#!/usr/bin/env python3
"""
Script to fetch 1000 real protein sequences from UniProt database.
Generates a comprehensive protein database for the CESGA API.
"""

import json
import urllib.request
import urllib.error
import time
from pathlib import Path

def fetch_from_uniprot(limit=1000):
    """Fetch real protein sequences from UniProt API."""
    
    print(f"Fetching {limit} proteins from UniProt...")
    
    # UniProt REST API query:
    # - Organism: Homo sapiens (Human)
    # - Format: JSON
    # - Fields: accession, id, protein name, sequence, length, organism_name
    url = (
        f"https://rest.uniprot.org/uniprotkb/search"
        f"?query=organism_id:9606%20AND%20reviewed:true"
        f"&format=json"
        f"&size={limit}"
        f"&fields=accession,id,protein_name,sequence,length,organism_name,gene_names,cc_function"
    )
    
    try:
        print(f"Querying: {url[:80]}...")
        
        # Add user agent header to comply with UniProt requirements
        headers = {'User-Agent': 'CESGA-API-Protein-Fetcher'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('results', [])
            
    except urllib.error.URLError as e:
        print(f"Network error: {e}")
        print("Will use fallback protein data instead...")
        return []
    except Exception as e:
        print(f"Error fetching from UniProt: {e}")
        return []


def parse_protein_from_uniprot(entry):
    """Parse UniProt JSON entry into our database format."""
    
    try:
        # Extract basic info
        uniprot_id = entry.get('primaryAccession', '')
        entry_id = entry.get('uniProtkbId', '')
        
        # Get protein names
        protein_name = entry_id.split('_')[0]  # Fallback
        if 'proteinDescription' in entry:
            names = entry['proteinDescription'].get('recommendedName', {})
            if names:
                protein_name = names.get('fullName', {}).get('value', protein_name)
        
        # Get sequence
        sequence = entry.get('sequence', {}).get('value', '')
        sequence_length = entry.get('sequence', {}).get('length', len(sequence))
        
        # Get organism
        organism = 'Homo sapiens'
        if 'organism' in entry:
            organism = entry['organism'].get('scientificName', organism)
        
        # Estimate molecular weight (average ~110 Da per amino acid)
        mol_weight = round(sequence_length * 0.11, 1)
        
        # Get function from comments
        function = "Protein with unknown function"
        if 'comments' in entry:
            for comment in entry.get('comments', []):
                if comment.get('commentType') == 'FUNCTION':
                    texts = comment.get('texts', [])
                    if texts:
                        function = texts[0].get('value', function)[:200]
                        break
        
        return {
            'uniprot_id': uniprot_id,
            'entry_id': entry_id,
            'protein_name': protein_name[:100],
            'organism': organism,
            'sequence': sequence,
            'length': sequence_length,
            'molecular_weight': mol_weight,
            'function': function,
            'source': 'UniProt',
            'pdb_id': '',  # Can be mapped later
            'cellular_location': 'Unknown',
            'known_structures': []
        }
    except Exception as e:
        print(f"Error parsing entry: {e}")
        return None


def generate_fallback_proteins(count=1000):
    """Generate synthetic but realistic protein data as fallback."""
    
    print(f"Generating {count} fallback protein sequences...")
    
    proteins = {}
    bases = "ACDEFGHIKLMNPQRSTVWY"  # Standard amino acids
    
    # Common protein prefixes and names
    prefixes = [
        "Nucleoporin", "Histone", "Kinase", "Phosphatase", "Transferase",
        "Hydrolase", "Ligase", "Isomerase", "ATPase", "GTPase",
        "Channel", "Transporter", "Receptor", "Antigen", "Antibody",
        "Collagen", "Keratin", "Elastin", "Fibrin", "Albumin"
    ]
    
    for i in range(count):
        # Generate realistic protein ID
        uniprot_id = f"P{str(i+1).zfill(5)}"
        entry_id = f"PROT{i+1:04d}_HUMAN"
        
        # Generate sequence (realistic length: 100-500 AA)
        length = 100 + (i % 400)
        sequence = ''.join(bases[i % len(bases)] for i in range(length))
        
        # Select protein class
        prefix = prefixes[(i // 50) % len(prefixes)]
        
        proteins[entry_id] = {
            'uniprot_id': uniprot_id,
            'entry_id': entry_id,
            'protein_name': f"{prefix} family protein {i+1}",
            'organism': 'Homo sapiens',
            'sequence': sequence,
            'length': length,
            'molecular_weight': round(length * 0.11, 1),
            'function': f"Member of {prefix} protein family",
            'source': 'Generated',
            'pdb_id': '',
            'cellular_location': 'Unknown',
            'known_structures': []
        }
    
    return proteins


def main():
    """Main function to generate protein database."""
    
    print("=" * 70)
    print("CESGA API - Protein Database Generator (1000+ proteins)")
    print("=" * 70)
    
    proteins = {}
    
    # Try fetching from UniProt
    uniprot_entries = fetch_from_uniprot(limit=1000)
    
    if uniprot_entries:
        print(f"Successfully fetched {len(uniprot_entries)} proteins from UniProt")
        
        for i, entry in enumerate(uniprot_entries):
            if (i + 1) % 100 == 0:
                print(f"Processing entry {i+1}/{len(uniprot_entries)}...")
            
            parsed = parse_protein_from_uniprot(entry)
            if parsed:
                key = parsed['entry_id']
                proteins[key] = parsed
    else:
        print("UniProt fetch failed, using generated proteins instead...")
    
    # If we don't have enough, generate more
    target_count = 1000
    if len(proteins) < target_count:
        needed = target_count - len(proteins)
        print(f"Need {needed} more proteins - generating...")
        
        fallback = generate_fallback_proteins(needed)
        proteins.update(fallback)
    
    print(f"\n✅ Total proteins in database: {len(proteins)}")
    
    # Save to file
    output_dir = Path(__file__).parent.parent / "app" / "services"
    output_file = output_dir / "protein_database_1000.json"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(proteins, f, indent=2)
    
    print(f"✅ Database saved to: {output_file}")
    print(f"   File size: {output_file.stat().st_size / (1024*1024):.1f} MB")
    
    # Generate summary
    print("\n📊 Database Summary:")
    print(f"   Total entries: {len(proteins)}")
    
    length_stats = [p['length'] for p in proteins.values()]
    print(f"   Protein length range: {min(length_stats)}-{max(length_stats)} AA")
    print(f"   Average length: {sum(length_stats)/len(length_stats):.0f} AA")
    
    sources = set(p.get('source', 'Unknown') for p in proteins.values())
    print(f"   Data sources: {', '.join(sources)}")
    
    # Print some examples
    print("\n📋 Sample entries:")
    for i, (key, protein) in enumerate(list(proteins.items())[:5]):
        print(f"\n   [{i+1}] {protein['protein_name']}")
        print(f"       UniProt: {protein['uniprot_id']} | Length: {protein['length']} AA")
        print(f"       Sequence: {protein['sequence'][:50]}...")

if __name__ == "__main__":
    main()
