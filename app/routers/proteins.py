"""Proteins catalog router — browse available proteins and their sequences."""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from app.services.real_protein_database import (
    REAL_PROTEINS_DATABASE,
    get_database_stats,
    get_sample_fasta_inputs,
)

router = APIRouter(prefix="/proteins", tags=["proteins catalog"])


class ProteinSummary(BaseModel):
    protein_id: str
    uniprot_id: str
    pdb_id: str
    protein_name: str
    organism: str
    length: int
    molecular_weight: float
    category: str
    description: str
    tags: List[str]


class ProteinDetail(BaseModel):
    protein_id: str
    uniprot_id: str
    pdb_id: str
    protein_name: str
    organism: str
    length: int
    molecular_weight: float
    isoelectric_point: float
    category: str
    description: str
    function: str
    cellular_location: str
    activity: str
    tags: List[str]
    sequence: str
    fasta_ready: str
    known_structures: List[dict]


class DatabaseStats(BaseModel):
    total_proteins: int
    embedded_proteins: int
    extended_proteins: int
    average_length: float
    min_length: int
    max_length: int
    by_category: dict


@router.get(
    "/",
    response_model=List[ProteinSummary],
    summary="List all proteins in the catalog",
    description=(
        "Returns all proteins available in the database. "
        "These are the sequences that will be **identified** by the API when submitted, "
        "returning real metadata (UniProt ID, PDB ID, organism) alongside structural predictions. "
        "Use `category` or `search` to filter."
    ),
)
def list_proteins(
    category: Optional[str] = Query(
        None,
        description="Filter by category: enzyme, transport, signaling, immune, hormone, reporter, structural, oncology, dna-replication",
    ),
    search: Optional[str] = Query(
        None,
        description="Search by name, organism, or tag (case-insensitive)",
    ),
    min_length: Optional[int] = Query(None, description="Minimum sequence length"),
    max_length: Optional[int] = Query(None, description="Maximum sequence length"),
):
    results = []
    for protein_id, data in REAL_PROTEINS_DATABASE.items():
        if category and data.get("category", "").lower() != category.lower():
            continue
        if min_length and data.get("length", 0) < min_length:
            continue
        if max_length and data.get("length", 0) > max_length:
            continue
        if search:
            s = search.lower()
            searchable = (
                data.get("protein_name", "").lower()
                + data.get("organism", "").lower()
                + data.get("description", "").lower()
                + " ".join(data.get("tags", [])).lower()
            )
            if s not in searchable:
                continue

        results.append(
            ProteinSummary(
                protein_id=protein_id,
                uniprot_id=data.get("uniprot_id", ""),
                pdb_id=data.get("pdb_id", ""),
                protein_name=data.get("protein_name", ""),
                organism=data.get("organism", ""),
                length=data.get("length", 0),
                molecular_weight=data.get("molecular_weight", 0.0),
                category=data.get("category", "unknown"),
                description=data.get("description", ""),
                tags=data.get("tags", []),
            )
        )

    return sorted(results, key=lambda p: p.length)


@router.get(
    "/stats",
    response_model=DatabaseStats,
    summary="Database statistics",
    description="Returns counts and statistics about the protein catalog.",
)
def database_stats():
    return get_database_stats()


@router.get(
    "/samples",
    summary="Get sample FASTA sequences ready to submit",
    description=(
        "Returns a list of copy-paste ready FASTA sequences for well-known proteins. "
        "These can be pasted directly into `POST /jobs/submit` as `fasta_sequence`."
    ),
)
def sample_fastas():
    samples = get_sample_fasta_inputs()
    result = []
    for fasta in samples:
        lines = fasta.strip().split("\n")
        header = lines[0]
        seq = "".join(lines[1:])
        # Extract protein name from header
        parts = header[1:].split(" ")
        uniprot_part = parts[0] if parts else ""
        name = " ".join(parts[1:]).split(" OS=")[0] if len(parts) > 1 else uniprot_part
        result.append({
            "protein_name": name,
            "uniprot_id": uniprot_part.split("|")[1] if "|" in uniprot_part else uniprot_part,
            "sequence_length": len(seq),
            "fasta": fasta.strip(),
        })
    return result


@router.get(
    "/{protein_id}",
    response_model=ProteinDetail,
    summary="Get full protein details + FASTA sequence",
    description=(
        "Returns complete information about a protein including its full sequence "
        "in FASTA format ready to submit to `POST /jobs/submit`. "
        "Use the `protein_id` from the list endpoint (e.g. `ubiquitin`, `gfp`, `calmodulin`)."
    ),
)
def get_protein(protein_id: str):
    data = REAL_PROTEINS_DATABASE.get(protein_id)
    if not data:
        raise HTTPException(
            status_code=404,
            detail=f"Protein '{protein_id}' not found. Use GET /proteins to see all available IDs.",
        )

    sequence = data.get("sequence", "")
    uniprot_id = data.get("uniprot_id", "")
    pdb_id = data.get("pdb_id", "")
    name = data.get("protein_name", "")
    organism = data.get("organism", "")

    # Build ready-to-use FASTA header (UniProt Swiss-Prot format)
    fasta_header = f">sp|{uniprot_id}|{protein_id.upper()} {name} OS={organism}"
    fasta_ready = f"{fasta_header}\n{sequence}"

    return ProteinDetail(
        protein_id=protein_id,
        uniprot_id=uniprot_id,
        pdb_id=pdb_id,
        protein_name=name,
        organism=organism,
        length=data.get("length", len(sequence)),
        molecular_weight=data.get("molecular_weight", 0.0),
        isoelectric_point=data.get("isoelectric_point", 0.0),
        category=data.get("category", "unknown"),
        description=data.get("description", ""),
        function=data.get("function", ""),
        cellular_location=data.get("cellular_location", ""),
        activity=data.get("activity", ""),
        tags=data.get("tags", []),
        sequence=sequence,
        fasta_ready=fasta_ready,
        known_structures=data.get("known_structures", []),
    )
