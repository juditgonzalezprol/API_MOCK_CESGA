"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum as PyEnum


class JobStatus(str, PyEnum):
    """Job status enumeration."""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class JobSubmitRequest(BaseModel):
    """Request schema for job submission endpoint."""
    fasta_sequence: str = Field(
        ...,
        min_length=1,
        max_length=100000,
        description="FASTA format protein sequence",
        example=">sequence1\nMKFSMVQ...",
    )
    fasta_filename: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Filename for the FASTA file",
        example="protein_seq.fasta",
    )
    gpus: int = Field(
        default=0,
        ge=0,
        le=4,
        description="Number of GPUs requested (max 4)",
    )
    cpus: int = Field(
        default=1,
        ge=1,
        le=64,
        description="Number of CPUs requested",
    )
    memory_gb: float = Field(
        default=4.0,
        gt=0,
        le=256,
        description="Memory requested in GB",
    )
    max_runtime_seconds: int = Field(
        default=3600,
        ge=60,
        le=86400,
        description="Maximum runtime in seconds (1 min - 24 hours)",
    )

    @field_validator("fasta_sequence")
    @classmethod
    def validate_fasta_format(cls, v):
        """Validate basic FASTA format."""
        lines = v.strip().split("\n")
        if not lines[0].startswith(">"):
            raise ValueError("FASTA sequence must start with '>'")
        if len(lines) < 2:
            raise ValueError("FASTA must contain a header and at least one sequence line")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "fasta_sequence": ">sp|P0CG47|UBC_HUMAN Ubiquitin\nMQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG",
                "fasta_filename": "ubiquitin.fasta",
                "gpus": 1,
                "cpus": 8,
                "memory_gb": 32.0,
                "max_runtime_seconds": 3600,
            }
        }
    }


class JobStatusResponse(BaseModel):
    """Response schema for status endpoint."""
    job_id: str = Field(..., validation_alias="id")
    status: JobStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    gpus: int
    cpus: int
    memory_gb: float
    max_runtime_seconds: int
    fasta_filename: str
    error_message: Optional[str] = None

    model_config = {"from_attributes": True, "populate_by_name": True}


class JobSubmitResponse(BaseModel):
    """Response schema for job submission."""
    job_id: str
    status: JobStatus = JobStatus.PENDING
    message: str = "Job submitted successfully"

    model_config = {
        "json_schema_extra": {
            "example": {
                "job_id": "job_abc123def456",
                "status": "PENDING",
                "message": "Job submitted successfully",
            }
        }
    }


class StructuralDataOutput(BaseModel):
    """Structural prediction data (PDB/CIF files + AlphaFold2 confidence metrics)."""
    pdb_file: Optional[str] = None
    cif_file: Optional[str] = None
    confidence: Dict[str, Any]  # pLDDT per residue, PAE matrix, histogram, mean


class ProteinMetadata(BaseModel):
    """Protein identification metadata."""
    identified_protein: Optional[str] = None
    uniprot_id: Optional[str] = None
    pdb_id: Optional[str] = None
    protein_name: Optional[str] = None
    organism: Optional[str] = None
    description: Optional[str] = None
    data_source: Optional[str] = None
    plddt_average: Optional[float] = None
    model_type: Optional[str] = None

    model_config = {"extra": "ignore"}


class SecondaryStructurePrediction(BaseModel):
    helix_percent: float
    strand_percent: float
    coil_percent: float


class SequenceProperties(BaseModel):
    length: int
    molecular_weight_kda: float
    positive_charges: int
    negative_charges: int
    cysteine_residues: int
    aromatic_residues: int


class BiologicalDataOutput(BaseModel):
    """Pre-calculated biological properties (solubility, stability, alerts, structure)."""
    solubility_score: float = Field(..., ge=0, le=100)
    solubility_prediction: Optional[str] = None
    instability_index: float
    stability_status: Optional[str] = None
    toxicity_alerts: List[str] = Field(default_factory=list)
    allergenicity_alerts: List[str] = Field(default_factory=list)
    secondary_structure_prediction: Optional[SecondaryStructurePrediction] = None
    sequence_properties: Optional[SequenceProperties] = None
    source: Optional[str] = None

    model_config = {"extra": "ignore"}


class JobOutputsResponse(BaseModel):
    """Response schema for job outputs endpoint."""
    job_id: str = Field(..., validation_alias="id")
    status: JobStatus
    protein_metadata: Optional[ProteinMetadata] = None
    structural_data: StructuralDataOutput
    biological_data: BiologicalDataOutput
    logs: str

    model_config = {"from_attributes": True, "populate_by_name": True}


class AccountingData(BaseModel):
    """Resource accounting — fictitious but realistic HPC usage metrics."""
    cpu_hours: float
    gpu_hours: float
    memory_gb_hours: float
    total_wall_time_seconds: int
    cpu_efficiency_percent: float = Field(..., ge=0, le=100)
    memory_efficiency_percent: float = Field(..., ge=0, le=100)
    gpu_efficiency_percent: Optional[float] = Field(None, ge=0, le=100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "cpu_hours": 8.5,
                "gpu_hours": 2.3,
                "memory_gb_hours": 128.0,
                "total_wall_time_seconds": 3600,
                "cpu_efficiency_percent": 85.5,
                "memory_efficiency_percent": 92.1,
                "gpu_efficiency_percent": 88.0,
            }
        }
    }


class JobAccountingResponse(BaseModel):
    """Response schema for accounting endpoint."""
    job_id: str = Field(..., validation_alias="id")
    status: JobStatus
    accounting: AccountingData

    model_config = {"from_attributes": True, "populate_by_name": True}
