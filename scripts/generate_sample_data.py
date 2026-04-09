#!/usr/bin/env python3
"""Generate standalone mock data files for testing."""
import json
from pathlib import Path
from app.services.mock_data_service import MockDataService

# Sample sequences
SEQUENCES = [
    {
        "name": "ubiquitin",
        "seq": "MQDRVIHIQAGQTGNSPKTAYQSIYDEKERY"
    },
    {
        "name": "insulin",
        "seq": "GIVEQCCTSICSLYQLENYCN"
    },
    {
        "name": "hemoglobin",
        "seq": "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTT"
    },
]


def main():
    """Generate mock data files."""
    output_dir = Path("app/mock_data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    mock_service = MockDataService()
    
    print("Generating mock data files...")
    
    for seq_data in SEQUENCES:
        seq = seq_data["seq"]
        name = seq_data["name"]
        
        # Confidence data
        conf_data = mock_service.generate_confidence_data(len(seq))
        conf_path = output_dir / f"{name}_confidence.json"
        with open(conf_path, 'w') as f:
            json.dump(conf_data, f, indent=2)
        print(f"✓ {conf_path}")
        
        # Biological data
        bio_data = mock_service.generate_biological_data(seq)
        bio_path = output_dir / f"{name}_biological.json"
        with open(bio_path, 'w') as f:
            json.dump(bio_data, f, indent=2)
        print(f"✓ {bio_path}")
        
        # Accounting data
        acct_data = mock_service.generate_accounting_data(3600, 1, 8, 32)
        acct_path = output_dir / f"{name}_accounting.json"
        with open(acct_path, 'w') as f:
            json.dump(acct_data, f, indent=2)
        print(f"✓ {acct_path}")
    
    print("\n✓ All mock data files generated!")


if __name__ == "__main__":
    main()
