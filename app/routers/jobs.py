"""Jobs router - API endpoints for job management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.schemas import (
    JobSubmitRequest,
    JobSubmitResponse,
    JobStatusResponse,
    JobOutputsResponse,
    JobAccountingResponse,
    StructuralDataOutput,
    BiologicalDataOutput,
    AccountingData,
    ProteinMetadata,
)
from app.models.db_models import Job, JobStatus
from app.services.job_service import JobService

router = APIRouter(prefix="/jobs", tags=["jobs"])
job_service = JobService()


@router.post(
    "/submit",
    response_model=JobSubmitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a new job",
    description="Submit a protein sequence in FASTA format for structure prediction.",
)
def submit_job(
    request: JobSubmitRequest,
    db: Session = Depends(get_db),
):
    """
    Submit a new job for AlphaFold2 structure prediction.
    
    - **fasta_sequence**: Protein sequence in FASTA format
    - **fasta_filename**: Name for the FASTA file
    - **gpus**: Number of GPUs (0-4)
    - **cpus**: Number of CPUs (1-64)
    - **memory_gb**: Memory in GB (0-256)
    - **max_runtime_seconds**: Max runtime in seconds (60-86400)
    """
    try:
        job = job_service.create_job(db, request)
        
        return JobSubmitResponse(
            job_id=job.id,
            status=JobStatus.PENDING,
            message="Job submitted successfully. Use the job_id to check status.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to submit job: {str(e)}",
        )


@router.get(
    "/{job_id}/status",
    response_model=JobStatusResponse,
    summary="Get job status",
    description="Get the current status and metadata of a job.",
)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db),
):
    """
    Get the current status of a job.
    
    Returns:
    - **job_id**: Unique job identifier
    - **status**: Current status (PENDING, RUNNING, COMPLETED, FAILED, CANCELLED)
    - **created_at**: Timestamp when job was created
    - **started_at**: Timestamp when job started running (null if not started)
    - **completed_at**: Timestamp when job completed (null if not completed)
    - **resource metadata**: GPUs, CPUs, memory requested
    - **error_message**: Error details if job failed
    """
    job = job_service.get_job(db, job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found",
        )
    
    # Convert ORM object to Pydantic with proper field mapping
    resp_data = {
        "id": job.id,  # This will map to job_id via alias
        "status": job.status,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "gpus": job.gpus,
        "cpus": job.cpus,
        "memory_gb": job.memory_gb,
        "max_runtime_seconds": job.max_runtime_seconds,
        "fasta_filename": job.fasta_filename,
        "error_message": job.error_message,
    }
    response_obj = JobStatusResponse.model_validate(resp_data)
    # Return the response object directly (FastAPI will serialize with field names)
    return response_obj


@router.get(
    "/{job_id}/outputs",
    response_model=JobOutputsResponse,
    summary="Get job outputs",
    description="Get structure files, confidence scores, and biological data (available only when COMPLETED).",
)
def get_job_outputs(
    job_id: str,
    db: Session = Depends(get_db),
):
    """
    Get the output files and results for a completed job.
    
    Only available when job status is COMPLETED.
    
    Returns:
    - **structural_data**: PDB/CIF files and confidence scores
    - **biological_data**: Solubility, instability, toxicity, allergenicity
    - **logs**: Standard output from the job execution
    """
    job = job_service.get_job(db, job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found",
        )
    
    if job.status != JobStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job outputs only available when status=COMPLETED. Current status: {job.status}",
        )
    
    try:
        outputs = job_service.get_job_outputs_dict(job)

        metadata_raw = outputs.get('protein_metadata')
        protein_metadata = ProteinMetadata(**metadata_raw) if metadata_raw else None

        return JobOutputsResponse(
            job_id=job.id,
            status=job.status,
            protein_metadata=protein_metadata,
            structural_data=StructuralDataOutput(
                pdb_file=outputs.get('pdb_file'),
                cif_file=outputs.get('cif_file'),
                confidence=outputs.get('confidence', {}),
            ),
            biological_data=BiologicalDataOutput(**outputs.get('biological_data', {})),
            logs=outputs.get('logs', ''),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve outputs: {str(e)}",
        )


@router.get(
    "/{job_id}/accounting",
    response_model=JobAccountingResponse,
    summary="Get job resource accounting",
    description="Get resource usage statistics for a job.",
)
def get_job_accounting(
    job_id: str,
    db: Session = Depends(get_db),
):
    """
    Get resource accounting information for a job.
    
    Returns fictitious but realistic resource consumption metrics:
    - **cpu_hours**: Total CPU-hours consumed
    - **gpu_hours**: Total GPU-hours (if GPUs were used)
    - **memory_gb_hours**: Memory-hours consumed
    - **total_wall_time_seconds**: Total elapsed time
    - **efficiency metrics**: CPU/memory/GPU utilization percentages
    """
    job = job_service.get_job(db, job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job {job_id} not found",
        )
    
    try:
        accounting_data = job_service.get_job_accounting(job)
        
        # Always should have data now, but handle gracefully
        if not accounting_data:
            # If somehow still empty, generate minimal data
            accounting_data = {
                "cpu_hours": 0.0,
                "gpu_hours": 0.0,
                "memory_gb_hours": 0.0,
                "total_wall_time_seconds": 0,
                "cpu_efficiency_percent": 0.0,
                "memory_efficiency_percent": 0.0,
            }
        
        return JobAccountingResponse(
            job_id=job.id,
            status=job.status,
            accounting=AccountingData(**accounting_data),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve accounting: {str(e)}",
        )


@router.get(
    "/",
    response_model=List[JobStatusResponse],
    summary="List all jobs",
    description="Get a list of all submitted jobs.",
)
def list_jobs(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    List all jobs with optional pagination.
    
    - **skip**: Number of jobs to skip
    - **limit**: Maximum number of jobs to return
    """
    jobs = db.query(Job).offset(skip).limit(limit).all()
    
    # Convert ORM objects to Pydantic with proper field mapping
    results = []
    for job in jobs:
        resp_data = {
            "id": job.id,  # This will map to job_id via alias
            "status": job.status,
            "created_at": job.created_at,
            "started_at": job.started_at,
            "completed_at": job.completed_at,
            "gpus": job.gpus,
            "cpus": job.cpus,
            "memory_gb": job.memory_gb,
            "max_runtime_seconds": job.max_runtime_seconds,
            "fasta_filename": job.fasta_filename,
            "error_message": job.error_message,
        }
        response_obj = JobStatusResponse.model_validate(resp_data)
        # Add the object (FastAPI will serialize automatically)
        results.append(response_obj)
    
    return results


