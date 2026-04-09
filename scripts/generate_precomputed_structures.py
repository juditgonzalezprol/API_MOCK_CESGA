"""Generate precomputed PDB files for known proteins."""
from pathlib import Path

# Real PDB coordinate data (simplified but realistic)
PDB_FILES = {
    "ubiquitin": """HEADER    UBIQUITIN                       17-JUN-84   1UBQ              
TITLE     THREE-DIMENSIONAL SOLUTION STRUCTURE OF UBIQUITIN
ATOM      1  N   ALA A   1      -8.901   4.127  -0.555  1.00  0.00           N
ATOM      2  CA  ALA A   1      -8.608   3.135  -1.618  1.00  0.00           C
ATOM      3  C   ALA A   1      -7.117   2.923  -1.897  1.00  0.00           C
ATOM      4  O   ALA A   1      -6.634   1.849  -1.758  1.00  0.00           O
ATOM      5  CB  ALA A   1      -9.437   3.396  -2.889  1.00  0.00           C
ATOM      6  N   MET A   2      -6.521   3.931  -2.224  1.00  0.00           N
ATOM      7  CA  MET A   2      -5.075   3.829  -2.353  1.00  0.00           C
ATOM      8  C   MET A   2      -4.561   2.850  -1.303  1.00  0.00           C
ATOM      9  O   MET A   2      -3.447   2.425  -1.355  1.00  0.00           O
ATOM     10  CB  MET A   2      -4.229   3.521  -3.616  1.00  0.00           C
END""",
    
    "hemoglobin_alpha": """HEADER    HEMOGLOBIN                      07-JUL-78   1HBA              
TITLE     THE CRYSTAL STRUCTURE OF HUMAN DEOXYHAEMOGLOBIN AT 1.74 
TITLE    2 ANGSTROMS RESOLUTION
REMARK    CHAIN A IS THE ALPHA SUBUNIT WITH HEME
ATOM      1  N   VAL A   1     -21.894   8.903   4.127  1.00 11.99           N
ATOM      2  CA  VAL A   1     -21.522   8.041   3.066  1.00 11.18           C
ATOM      3  C   VAL A   1     -20.098   8.158   2.553  1.00 10.22           C
ATOM      4  O   VAL A   1     -19.733   9.116   1.885  1.00 10.48           O
ATOM      5  CB  VAL A   1     -22.480   8.183   1.909  1.00 13.27           C
HETATM 1203 FE   HEM A 143       1.914  -0.215  -1.856  1.00 14.08          FE
END""",
    
    "lysozyme": """HEADER    HYDROLASE/HYDROLASE INHIBITOR       06-MAR-84   1LYZ              
TITLE     CRYSTAL STRUCTURE OF CHICKEN LYSOZYME
ATOM      1  N   MET A   1     -31.740  20.154  29.699  1.00 44.04           N
ATOM      2  CA  MET A   1     -30.906  20.533  28.566  1.00 15.19           C
ATOM      3  C   MET A   1     -31.758  20.139  27.330  1.00 13.84           C
ATOM      4  O   MET A   1     -31.340  19.504  26.328  1.00 12.66           O
ATOM      5  CB  MET A   1     -29.553  19.921  28.452  1.00 15.11           C
ATOM      6  N   ARG A   2     -32.944  20.590  27.528  1.00 15.39           N
ATOM      7  CA  ARG A   2     -33.827  20.286  26.408  1.00 15.46           C
END""",
}

def generate_precomputed_pdb_files():
    """Generate PDB files for known proteins."""
    output_dir = Path("/Users/juditgonzalez/Desktop/API_CESGA/app/mock_data/precomputed")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for protein_name, pdb_content in PDB_FILES.items():
        pdb_file = output_dir / f"{protein_name}.pdb"
        pdb_file.write_text(pdb_content)
        print(f"Created: {pdb_file}")

if __name__ == "__main__":
    generate_precomputed_pdb_files()
