"""Job management service - core business logic."""
import uuid
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from sqlalchemy.orm import Session
from app.models.db_models import Job, JobStatus
from app.models.schemas import JobSubmitRequest
from app.services.mock_data_service import MockDataService
from app.services.real_protein_database import get_all_proteins
from app.services.alphafold_service import get_alphafold_service

logger = logging.getLogger(__name__)


class JobService:
    """Service for managing jobs lifecycle."""
    
    RESULTS_DIR = Path("app/mock_data/sample_results")
    PRECOMPUTED_DIR = Path("app/mock_data/precomputed")
    
    def __init__(self):
        """Initialize service."""
        self.mock_service = MockDataService()
        self.RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        self.PRECOMPUTED_DIR.mkdir(parents=True, exist_ok=True)
        self.known_proteins = get_all_proteins()
    
    def _identify_protein(self, fasta_sequence: str) -> Optional[tuple]:
        """Identify if sequence matches a known protein.
        
        Returns:
            Tuple of (protein_name, protein_data) or None
        """
        # Extract sequence without header
        seq_lines = [l.strip() for l in fasta_sequence.split('\n') 
                     if l.strip() and not l.startswith('>')]
        sequence_clean = ''.join(seq_lines).upper()
        
        # Try exact match
        for name, data in self.known_proteins.items():
            known_seq = data["sequence"].upper()
            if sequence_clean == known_seq or known_seq in sequence_clean or sequence_clean in known_seq:
                return (name, data)
        
        return None
    
    def create_job(self, db: Session, request: JobSubmitRequest) -> Job:
        """Create a new job in the database."""
        job_id = self._generate_job_id()
        
        job = Job(
            id=job_id,
            fasta_sequence=request.fasta_sequence,
            fasta_filename=request.fasta_filename,
            gpus=request.gpus,
            cpus=request.cpus,
            memory_gb=request.memory_gb,
            max_runtime_seconds=request.max_runtime_seconds,
            status=JobStatus.PENDING,
            created_at=datetime.utcnow(),
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        
        return job
    
    def get_job(self, db: Session, job_id: str) -> Optional[Job]:
        """Retrieve a job by ID."""
        return db.query(Job).filter(Job.id == job_id).first()
    
    def update_job_status(
        self,
        db: Session,
        job_id: str,
        new_status: JobStatus,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
    ) -> Optional[Job]:
        """Update job status."""
        job = self.get_job(db, job_id)
        if not job:
            return None
        
        job.status = new_status
        if started_at:
            job.started_at = started_at
        if completed_at:
            job.completed_at = completed_at
        
        db.commit()
        db.refresh(job)
        return job
    
    def Mark_job_running(self, db: Session, job_id: str) -> Optional[Job]:
        """Mark a job as RUNNING."""
        return self.update_job_status(
            db, job_id, JobStatus.RUNNING, started_at=datetime.utcnow()
        )
    
    def mark_job_completed(self, db: Session, job_id: str) -> Optional[Job]:
        """Mark a job as COMPLETED and generate output files."""
        job = self.get_job(db, job_id)
        if not job:
            return None
        
        # Calculate elapsed time
        elapsed_seconds = (datetime.utcnow() - job.started_at).total_seconds() \
            if job.started_at else 10
        
        # Generate output data
        self._generate_job_outputs(job, elapsed_seconds)
        
        # Update job status
        return self.update_job_status(
            db, job_id, JobStatus.COMPLETED, completed_at=datetime.utcnow()
        )
    
    def _generate_job_outputs(self, job: Job, elapsed_seconds: float) -> None:
        """Generate output files for a job.
        
        Priority:
        1. Use AlphaFold DB if sequence found in UniProt
        2. Use precomputed PDB if known protein
        3. Generate synthetic data
        """
        job_dir = self.RESULTS_DIR / job.id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract sequence
        seq_lines = [l.strip() for l in job.fasta_sequence.split('\n') 
                     if l.strip() and not l.startswith('>')]
        sequence_clean = ''.join(seq_lines)
        
        # Try AlphaFold DB first
        alphafold_service = get_alphafold_service()
        alphafold_result = alphafold_service.predict_structure_from_sequence(job.fasta_sequence)
        
        if alphafold_result and alphafold_result.get('pipeline_success'):
            # Use AlphaFold prediction
            logger.info(f"Using AlphaFold DB prediction for job {job.id}")
            
            # Save PDB with AlphaFold data
            pdb_content = alphafold_result['pdb_content']
            pdb_path = job_dir / "structure.pdb"
            pdb_path.write_text(pdb_content)
            job.output_pdb_path = str(pdb_path)
            
            # Generate mmCIF (use mock for now, as AlphaFold DB doesn't provide CIF in API)
            cif_content = self.mock_service.generate_mmcif_structure(job.fasta_sequence)
            cif_path = job_dir / "structure.cif"
            cif_path.write_text(cif_content)
            job.output_cif_path = str(cif_path)
            
            # Use pLDDT confidence data from AlphaFold
            avg_plddt = alphafold_result.get('avg_plddt', 75.0)
            plddt_scores = alphafold_result.get('plddt_scores', [])
            
            # Store confidence metrics
            confidence_data = {
                "plddt": avg_plddt,
                "plddt_scores": plddt_scores[:100] if plddt_scores else [],  # Sample
                "confidence_category": alphafold_result.get('confidence', 'Medium'),
                "model_type": alphafold_result.get('model_type', 'AF2-monomer'),
                "source": "AlphaFold DB",
                "uniprot_id": alphafold_result.get('uniprot_id', ''),
            }
            
            confidence_path = job_dir / "confidence.json"
            with open(confidence_path, 'w') as f:
                json.dump(confidence_data, f, indent=2)
            job.confidence_json_path = str(confidence_path)
            
            # Store protein metadata
            metadata = {
                "identified_protein": alphafold_result.get('protein_name', 'Unknown'),
                "uniprot_id": alphafold_result.get('uniprot_id', ''),
                "organism": alphafold_result.get('organism', 'Unknown'),
                "data_source": "AlphaFold Database",
                "plddt_average": avg_plddt,
                "model_type": alphafold_result.get('model_type', 'AF2-monomer'),
            }
            metadata_path = job_dir / "protein_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        else:
            # Fallback: Try precomputed or generate synthetic
            logger.info(f"AlphaFold not available, using fallback for job {job.id}")
            
            # Try to identify if it's a known protein
            protein_info = self._identify_protein(job.fasta_sequence)
            protein_name = protein_info[0] if protein_info else None
            
            # Generate or copy PDB structure
            precomputed_pdb = self.PRECOMPUTED_DIR / f"{protein_name}.pdb"
            if protein_info and precomputed_pdb.exists():
                # Use precomputed PDB
                pdb_content = precomputed_pdb.read_text()
            else:
                # Generate synthetic PDB
                pdb_content = self.mock_service.generate_pdb_structure(job.fasta_sequence)
            
            pdb_path = job_dir / "structure.pdb"
            pdb_path.write_text(pdb_content)
            job.output_pdb_path = str(pdb_path)
            
            # Generate mmCIF structure
            cif_content = self.mock_service.generate_mmcif_structure(job.fasta_sequence)
            cif_path = job_dir / "structure.cif"
            cif_path.write_text(cif_content)
            job.output_cif_path = str(cif_path)
            
            # Generate confidence data
            confidence_data = self.mock_service.generate_confidence_data(len(sequence_clean))
            confidence_path = job_dir / "confidence.json"
            with open(confidence_path, 'w') as f:
                json.dump(confidence_data, f, indent=2)
            job.confidence_json_path = str(confidence_path)
            
            # Try to add protein info metadata
            if protein_info:
                metadata = {
                    "identified_protein": protein_info[0],
                    "uniprot_id": protein_info[1].get("uniprot_id"),
                    "pdb_id": protein_info[1].get("pdb_id"),
                    "protein_name": protein_info[1].get("protein_name"),
                    "organism": protein_info[1].get("organism"),
                    "description": protein_info[1].get("description"),
                    "known_structures": protein_info[1].get("known_structures", []),
                    "data_source": "precomputed_database"
                }
                metadata_path = job_dir / "protein_metadata.json"
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
        
        # Common outputs (for both paths)
        # Generate biological data
        bio_data = self.mock_service.generate_biological_data(sequence_clean)
        bio_path = job_dir / "biological_properties.json"
        with open(bio_path, 'w') as f:
            json.dump(bio_data, f, indent=2)
        job.biological_data_path = str(bio_path)
        
        # Generate logs
        logs_content = self.mock_service.generate_logs()
        logs_path = job_dir / "slurm_output.log"
        logs_path.write_text(logs_content)
        job.logs_path = str(logs_path)
        
        # Generate accounting data
        accounting_data = self.mock_service.generate_accounting_data(
            int(elapsed_seconds),
            job.gpus,
            job.cpus,
            job.memory_gb,
        )
        accounting_path = job_dir / "accounting.json"
        with open(accounting_path, 'w') as f:
            json.dump(accounting_data, f, indent=2)
        job.accounting_data_path = str(accounting_path)
    
    def get_job_outputs_dict(self, job: Job) -> dict:
        """Retrieve all output files for a completed job."""
        outputs = {}

        if job.output_pdb_path and Path(job.output_pdb_path).exists():
            with open(job.output_pdb_path) as f:
                outputs['pdb_file'] = f.read()

        if job.output_cif_path and Path(job.output_cif_path).exists():
            with open(job.output_cif_path) as f:
                outputs['cif_file'] = f.read()

        if job.confidence_json_path and Path(job.confidence_json_path).exists():
            with open(job.confidence_json_path) as f:
                outputs['confidence'] = json.load(f)

        if job.biological_data_path and Path(job.biological_data_path).exists():
            with open(job.biological_data_path) as f:
                outputs['biological_data'] = json.load(f)

        if job.logs_path and Path(job.logs_path).exists():
            with open(job.logs_path) as f:
                outputs['logs'] = f.read()

        # Load protein metadata if present (stored alongside other outputs)
        metadata_path = self.RESULTS_DIR / job.id / "protein_metadata.json"
        if metadata_path.exists():
            with open(metadata_path) as f:
                outputs['protein_metadata'] = json.load(f)

        return outputs
    
    def get_job_accounting(self, job: Job) -> dict:
        """Retrieve or generate accounting data for a job."""
        # Try to load from existing file
        if job.accounting_data_path and Path(job.accounting_data_path).exists():
            with open(job.accounting_data_path) as f:
                return json.load(f)
        
        # If no saved data, generate mock accounting based on job elapsed time
        elapsed_seconds = 0
        if job.started_at:
            if job.completed_at:
                elapsed_seconds = int((job.completed_at - job.started_at).total_seconds())
            else:
                # Job is still running - estimate time since start
                elapsed_seconds = int((datetime.utcnow() - job.started_at).total_seconds())
        else:
            # Job hasn't started yet - use minimal time
            elapsed_seconds = 5
        
        # Generate mock accounting data
        accounting_data = self.mock_service.generate_accounting_data(
            max(elapsed_seconds, 1),  # At least 1 second
            job.gpus,
            job.cpus,
            job.memory_gb,
        )
        
        return accounting_data if accounting_data else {}
    
    @staticmethod
    def _generate_job_id() -> str:
        """Generate a unique job ID similar to Slurm."""
        return f"job_{uuid.uuid4().hex[:12]}"
