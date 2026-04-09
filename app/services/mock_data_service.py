"""Mock data generation service for synthetic AlphaFold2 results."""
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
import numpy as np
from app.services.real_protein_database import (
    get_protein_properties,
    get_protein_alerts,
    search_protein_by_uniprot,
)


class MockDataService:
    """Generate realistic mock AlphaFold2 prediction data."""
    
    @staticmethod
    def generate_confidence_data(sequence_length: int) -> Dict[str, Any]:
        """Generate realistic pLDDT and PAE data."""
        # pLDDT: per-residue confidence (0-100, higher is better)
        plddt_scores = np.random.uniform(40, 95, sequence_length).tolist()
        
        # Create realistic pLDDT distribution (higher at termini, variable in middle)
        for i in range(sequence_length):
            if i < sequence_length * 0.1 or i > sequence_length * 0.9:
                plddt_scores[i] = min(95, plddt_scores[i] + 10)
        
        # PAE: Predicted Aligned Error matrix (lower is better, typically 0-32)
        pae_matrix = []
        for i in range(min(sequence_length, 384)):  # PAE typically trimmed for large sequences
            row = []
            for j in range(min(sequence_length, 384)):
                # Higher error for distant residues
                distance = abs(i - j)
                base_error = min(30, distance * 0.05 + 2)
                error = base_error + np.random.normal(0, 2)
                row.append(max(0, min(32, error)))
            pae_matrix.append(row)
        
        return {
            "plddt_per_residue": plddt_scores,
            "plddt_histogram": {
                "very_high": sum(1 for s in plddt_scores if s > 90),
                "high": sum(1 for s in plddt_scores if 70 < s <= 90),
                "medium": sum(1 for s in plddt_scores if 50 < s <= 70),
                "low": sum(1 for s in plddt_scores if s <= 50),
            },
            "pae_matrix": pae_matrix,
            "mean_pae": np.mean(pae_matrix) if pae_matrix else 0,
            "plddt_mean": np.mean(plddt_scores),
        }
    
    @staticmethod
    def generate_pdb_structure(sequence: str) -> str:
        """Generate a minimal realistic PDB file."""
        lines = []
        lines.append("HEADER    SIMULATED ALPHAFOLD STRUCTURE")
        lines.append(f"TITLE     AlphaFold2 Simulation for {len(sequence)} residues")
        lines.append(f"REMARK   1 REFERENCE 1")
        lines.append(f"REMARK   2 RESOLUTION.    NONE.")
        lines.append(f"ATOM             X       Y       Z     CONF")
        
        # Simple alpha-helix-like coordinates
        residues = [line.strip() for line in sequence.split('\n') if line.strip() and not line.startswith('>')]
        seq = ''.join(residues)
        
        atom_count = 1
        for i, aa in enumerate(seq[:384]):  # Limit to 384 residues as AlphaFold does
            # Simple helix coordinates
            x = 10 * np.cos(i * 0.1)
            y = i * 1.5
            z = 10 * np.sin(i * 0.1)
            plddt = random.uniform(50, 95)
            
            lines.append(
                f"ATOM  {atom_count:5d}  CA  ALA {i+1:4d}    "
                f"{x:8.3f}{y:8.3f}{z:8.3f}  1.00{plddt:6.2f}           C"
            )
            atom_count += 1
        
        lines.append("END")
        return "\n".join(lines)
    
    @staticmethod
    def generate_mmcif_structure(sequence: str) -> str:
        """Generate a minimal mmCIF file."""
        residues = [line.strip() for line in sequence.split('\n') if line.strip() and not line.startswith('>')]
        seq = ''.join(residues)
        num_residues = len(seq)
        
        lines = [
            "data_simulated_structure",
            "_entry.id   SIM001",
            f"_struct.title   'AlphaFold2 Simulation for {num_residues} residues'",
            "_struct.pdbx_descriptor   'AlphaFold2 predicted model'",
            "",
            "loop_",
            "_atom_site.group_PDB",
            "_atom_site.id",
            "_atom_site.type_symbol",
            "_atom_site.label_atom_id",
            "_atom_site.label_comp_id",
            "_atom_site.label_asym_id",
            "_atom_site.label_entity_id",
            "_atom_site.label_seq_id",
            "_atom_site.Cartn_x",
            "_atom_site.Cartn_y",
            "_atom_site.Cartn_z",
            "_atom_site.B_iso_or_equiv",
        ]
        
        for i in range(min(num_residues, 384)):
            x = 10 * np.cos(i * 0.1)
            y = i * 1.5
            z = 10 * np.sin(i * 0.1)
            plddt = random.uniform(50, 95)
            
            lines.append(
                f"ATOM {i+1:6d} C CA ALA A 1 {i+1:4d} "
                f"{x:8.3f} {y:8.3f} {z:8.3f} {plddt:6.2f}"
            )
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_biological_data(sequence: str, protein_name: str = None) -> Dict[str, Any]:
        """Generate bioinformatics predictions.
        
        Uses real data if protein_name is provided and matches a known protein,
        otherwise generates synthetic data based on sequence properties.
        """
        # Try to get real data if protein name provided
        if protein_name:
            real_properties = get_protein_properties(protein_name)
            if real_properties:
                real_alerts = get_protein_alerts(protein_name)
                return {
                    **real_properties,
                    "toxicity_alerts": real_alerts.get("toxicity_alerts", []),
                    "allergenicity_alerts": real_alerts.get("allergenicity_alerts", []),
                    "source": "real_data",
                }
        
        # Generate synthetic bioinformatics predictions based on sequence
        # Solubility: heuristic based on amino acid composition
        aa_comp = {}
        for aa in sequence.upper():
            if aa in "ACDEFGHIKLMNPQRSTVWY":
                aa_comp[aa] = aa_comp.get(aa, 0) + 1
        
        if len(sequence) == 0:
            return {"error": "Empty sequence"}
        
        # Hydrophobic aa: A, V, I, L, M, F, W
        hydrophobic_fraction = sum(aa_comp.get(aa, 0) for aa in "AVILMFW") / len(sequence)
        solubility_score = 100 - (hydrophobic_fraction * 80) + random.uniform(-10, 10)
        
        # Instability Index (Guruprasad et al.) - use Kyte-Doolittle scale
        ii_score = 0
        aa_scale = {
            "A": 0.62, "C": 1.19, "D": 0.69, "E": 0.74, "F": 1.06,
            "G": 0.57, "H": 0.87, "I": 1.08, "K": 0.77, "L": 1.15,
            "M": 1.45, "N": 0.67, "P": 0.36, "Q": 0.93, "R": 0.98,
            "S": 0.77, "T": 0.83, "V": 1.06, "W": 1.08, "Y": 0.69
        }
        
        # Calculate instability based on dipeptide composition (simplified)
        for i in range(len(sequence) - 1):
            aa1 = sequence[i].upper()
            aa2 = sequence[i + 1].upper()
            if aa1 in aa_scale and aa2 in aa_scale:
                ii_score += abs(aa_scale.get(aa1, 0.7) - aa_scale.get(aa2, 0.7))
        
        instability_index = (ii_score / len(sequence)) * 10 + random.uniform(15, 25)
        instability_status = "stable" if instability_index < 40 else "unstable"
        
        # Secondary structure prediction (Kabat-Labhardt rules)
        charged_positive = sum(1 for aa in sequence.upper() if aa in "KR")
        charged_negative = sum(1 for aa in sequence.upper() if aa in "DE")
        aromatic = sum(1 for aa in sequence.upper() if aa in "FYW")
        helix_prone = sum(1 for aa in sequence.upper() if aa in "AELM")
        
        helix_percent = (helix_prone / len(sequence)) * 100
        strand_percent = (charged_negative / len(sequence)) * 100
        coil_percent = 100 - helix_percent - strand_percent
        
        # Toxicity alerts (based on sequence motifs)
        toxicity_alerts = []
        # Signal peptide signature:
        if sequence[:20].count("M") > 0 and any(aa in sequence[:10].upper() for aa in "AGLVS"):
            toxicity_alerts.append("Potential signal peptide detected (Kozak sequence motif)")
        # Protease cleavage sites:
        if "RR" in sequence.upper() or "KK" in sequence.upper():
            toxicity_alerts.append("Potential protease cleavage site (dibasic motif) detected")
        # Disulfide bonds:
        if sequence.count("C") > 2:
            toxicity_alerts.append(f"{sequence.count('C')} cysteine residues detected - may form disulfide bonds")
        
        # Allergenicity alerts (based on known allergen motifs)
        allergenicity_alerts = []
        if len(sequence) > 100:
            allergenicity_alerts.append("Protein length > 100 aa (typical allergen size range)")
        if charged_positive > len(sequence) * 0.15:
            allergenicity_alerts.append("High positive charge content (potential allergen epitope)")
        # Check for common allergen epitopes
        if "QQQQ" in sequence.upper() or "KKKK" in sequence.upper():
            allergenicity_alerts.append("Repetitive charge clusters detected (potential IgE epitope)")
        
        return {
            "solubility_score": max(0, min(100, solubility_score)),
            "solubility_prediction": "soluble" if solubility_score > 50 else "poorly soluble",
            "instability_index": round(instability_index, 2),
            "stability_status": instability_status,
            "toxicity_alerts": toxicity_alerts,
            "allergenicity_alerts": allergenicity_alerts,
            "secondary_structure_prediction": {
                "helix_percent": round(helix_percent, 1),
                "strand_percent": round(strand_percent, 1),
                "coil_percent": round(coil_percent, 1),
            },
            "sequence_properties": {
                "length": len(sequence),
                "molecular_weight_kda": round(len(sequence) * 0.11, 1),  # Approximate MW
                "positive_charges": charged_positive,
                "negative_charges": charged_negative,
                "cysteine_residues": sequence.count("C"),
                "aromatic_residues": aromatic,
            },
            "source": "synthetic_prediction",
        }
    
    @staticmethod
    def generate_logs() -> str:
        """Generate realistic Apptainer/container simulation logs."""
        logs = []
        logs.append(f"[{datetime.now().isoformat()}] Job started in Apptainer container")
        logs.append("[INFO] Loading AlphaFold2 model weights...")
        logs.append("[INFO] Model weights loaded successfully")
        logs.append("[INFO] Generating multiple sequence alignment (MSA)...")
        logs.append("[INFO] MSA generation at 25%...")
        logs.append("[INFO] MSA generation at 50%...")
        logs.append("[INFO] MSA generation at 75%...")
        logs.append("[INFO] MSA generation at 100%")
        logs.append("[INFO] Running AlphaFold2 inference...")
        logs.append("[WARNING] GPU memory utilization: 89%")
        logs.append("[INFO] Prediction confidence (pLDDT) distribution: mean=75.3, std=12.1")
        logs.append("[INFO] Iterative refinement...")
        logs.append("[INFO] Model evaluation complete")
        logs.append("[INFO] Saving structure to PDB format")
        logs.append(f"[{datetime.now().isoformat()}] Job completed successfully")
        
        return "\n".join(logs)
    
    @staticmethod
    def generate_accounting_data(
        total_seconds: int,
        gpus: int,
        cpus: int,
        memory_gb: float,
    ) -> Dict[str, Any]:
        """Generate realistic resource accounting."""
        total_hours = total_seconds / 3600
        
        # Simulate realistic GPU/CPU utilization
        gpu_utilization = random.uniform(75, 95) / 100
        cpu_utilization = random.uniform(40, 70) / 100
        memory_utilization = random.uniform(60, 85) / 100
        
        gpu_hours = (gpus * total_hours * gpu_utilization) if gpus > 0 else 0
        cpu_hours = cpus * total_hours * cpu_utilization
        memory_hours = memory_gb * total_hours * memory_utilization
        
        return {
            "cpu_hours": cpu_hours,
            "gpu_hours": gpu_hours,
            "memory_gb_hours": memory_hours,
            "total_wall_time_seconds": total_seconds,
            "cpu_efficiency_percent": cpu_utilization * 100,
            "memory_efficiency_percent": memory_utilization * 100,
            "gpu_efficiency_percent": (gpu_utilization * 100) if gpus > 0 else 0,
        }
