#!/usr/bin/env python3
"""Initialize database with sample completed jobs for testing."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base
from app.models.db_models import Job, JobStatus
from app.services.job_service import JobService
from app.services.mock_data_service import MockDataService

# Sample FASTA sequences for testing
SAMPLE_SEQUENCES = [
    {
        "id": "sample_001",
        "filename": "ubiquitin.fasta",
        "sequence": """>sp|P0CG47|UBA1_HUMAN Ubiquitin
MQDRVIHIQAGQTGNSPKTAYQSIYDEKERY"""
    },
    {
        "id": "sample_002",
        "filename": "insulin.fasta",
        "sequence": """>sp|P01308|INS_HUMAN Insulin A and B chain
GIVEQCCTSICSLYQLENYCN"""
    },
    {
        "id": "sample_003",
        "filename": "hsa_hemoglobin.fasta",
        "sequence": """>sp|P69905|HBA_HUMAN Hemoglobin subunit alpha
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTT"""
    },
]


def initialize_database():
    """Create database tables."""
    engine = create_engine(
        settings.database_url,
        echo=True,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    print(f"✓ Database tables created at {settings.database_url}")
    return engine


def create_sample_completed_jobs(engine):
    """Create sample completed jobs with pre-generated results."""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    job_service = JobService()
    mock_service = MockDataService()
    results_dir = Path("app/mock_data/sample_results")
    results_dir.mkdir(parents=True, exist_ok=True)
    
    now = datetime.utcnow()
    
    for idx, sample in enumerate(SAMPLE_SEQUENCES):
        # Create job record
        job = Job(
            id=sample["id"],
            fasta_sequence=sample["sequence"],
            fasta_filename=sample["filename"],
            gpus=1,
            cpus=8,
            memory_gb=32.0,
            max_runtime_seconds=3600,
            status=JobStatus.COMPLETED,
            created_at=now - timedelta(hours=2),
            started_at=now - timedelta(minutes=30),
            completed_at=now - timedelta(minutes=5),
        )
        
        db.add(job)
        db.flush()  # Get the job ID
        
        # Generate outputs
        job_dir = results_dir / job.id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract sequence
        seq_lines = [l.strip() for l in sample["sequence"].split('\n') 
                     if l.strip() and not l.startswith('>')]
        sequence_clean = ''.join(seq_lines)
        
        # PDB file
        pdb_content = mock_service.generate_pdb_structure(sample["sequence"])
        pdb_path = job_dir / "structure.pdb"
        pdb_path.write_text(pdb_content)
        job.output_pdb_path = str(pdb_path.relative_to(Path.cwd()))
        
        # CIF file
        cif_content = mock_service.generate_mmcif_structure(sample["sequence"])
        cif_path = job_dir / "structure.cif"
        cif_path.write_text(cif_content)
        job.output_cif_path = str(cif_path.relative_to(Path.cwd()))
        
        # Confidence data
        confidence_data = mock_service.generate_confidence_data(len(sequence_clean))
        confidence_path = job_dir / "confidence.json"
        with open(confidence_path, 'w') as f:
            json.dump(confidence_data, f, indent=2)
        job.confidence_json_path = str(confidence_path.relative_to(Path.cwd()))
        
        # Biological data
        bio_data = mock_service.generate_biological_data(sequence_clean)
        bio_path = job_dir / "biological_properties.json"
        with open(bio_path, 'w') as f:
            json.dump(bio_data, f, indent=2)
        job.biological_data_path = str(bio_path.relative_to(Path.cwd()))
        
        # Logs
        logs_content = mock_service.generate_logs()
        logs_path = job_dir / "slurm_output.log"
        logs_path.write_text(logs_content)
        job.logs_path = str(logs_path.relative_to(Path.cwd()))
        
        # Accounting data
        elapsed_seconds = 1500  # 25 minutes
        accounting_data = mock_service.generate_accounting_data(
            elapsed_seconds, job.gpus, job.cpus, job.memory_gb
        )
        accounting_path = job_dir / "accounting.json"
        with open(accounting_path, 'w') as f:
            json.dump(accounting_data, f, indent=2)
        job.accounting_data_path = str(accounting_path.relative_to(Path.cwd()))
        
        db.commit()
        print(f"✓ Created sample job {job.id} ({sample['filename']})")
    
    db.close()


def main():
    """Main initialization flow."""
    print("=" * 60)
    print("CESGA API Simulator - Database Initialization")
    print("=" * 60)
    
    # Initialize database tables
    engine = initialize_database()
    
    # Create sample data
    print("\nCreating sample completed jobs...")
    create_sample_completed_jobs(engine)
    
    print("\n" + "=" * 60)
    print("✓ Database initialization complete!")
    print("=" * 60)
    print("\nTesting:")
    print("1. Start the API: python -m uvicorn app.main:app --reload")
    print("2. View Swagger docs: http://localhost:8000/docs")
    print(f"3. Test sample jobs:")
    for sample in SAMPLE_SEQUENCES:
        print(f"   - curl http://localhost:8000/jobs/{sample['id']}/status")


if __name__ == "__main__":
    main()
