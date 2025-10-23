import subprocess
import json
import pandas as pd
import os
from collections import defaultdict
from pathlib import Path

# BINANA Configuration
# Updated to use the streamlined BINANA version
binana = '/home/davis/projects/binana/python/run_binana.py'
receptor_pdbqt = 'receptorH.pdbqt'
ligand_pdbqt   = 'ligand_1.pdbqt'
output_dir = './binana_results/'  # Changed to use a specific directory

# Display Configuration
SHOW_DETAILED_OUTPUT = True   # Set to False for quiet mode (only show summary)
# SHOW_DETAILED_OUTPUT = False  # Uncomment this line for quiet mode

def run_binana_analysis(show_output=True):
    """Run BINANA analysis with proper error handling
    
    Args:
        show_output (bool): If True, shows BINANA's detailed output in terminal
                          If False, runs silently and only shows summary
    """
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Created output directory: {output_dir}")
    
    # Check if input files exist
    if not os.path.exists(receptor_pdbqt):
        raise FileNotFoundError(f"Receptor file not found: {receptor_pdbqt}")
    if not os.path.exists(ligand_pdbqt):
        raise FileNotFoundError(f"Ligand file not found: {ligand_pdbqt}")
    
    command = [
        "python3", binana,
        "-receptor", receptor_pdbqt,  # Fixed parameter name (remove --)
        "-ligand", ligand_pdbqt,      # Fixed parameter name (remove --)
        "-output_dir", output_dir,
    ]
    
    print("Running BINANA analysis...")
    print(f"Command: {' '.join(command)}")
    
    if show_output:
        print("=" * 60)
        print("BINANA DETAILED OUTPUT:")
        print("=" * 60)
    
    try:
        if show_output:
            # Show all BINANA output in real-time
            result = subprocess.run(command, check=True)
        else:
            # Run silently, only capture errors
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print("=" * 60)
        print("BINANA analysis completed!")
        print("=" * 60)
        return True
    except subprocess.CalledProcessError as e:
        print(f"BINANA failed with error: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Error output: {e.stderr}")
        return False

# Run BINANA analysis
if run_binana_analysis(show_output=SHOW_DETAILED_OUTPUT):
    # Process BINANA output and generate CSV
    output_json_path = os.path.join(output_dir, 'output.json')
    
    print(f"Reading BINANA results from: {output_json_path}")
    
    with open(output_json_path, 'r') as f:
        binana_data = json.load(f)

        interaction_keys = {
            "hydrogen_bonds": "hydrogenBonds",
            "salt_bridges": "saltBridges",
            "hydrophobic_contacts": "hydrophobicContacts",
            "pi_pi_stackings": "piStackings",
            "pi_cation_interactions": "piCationInteractions",
            "metal_complexes": "metalComplexes",
            "close_contacts": "closeContacts"
        }

        receptor_residue_summary = defaultdict(set)

        for interaction_name, json_key in interaction_keys.items():
            interactions = binana_data.get(json_key, [])

            for entry in interactions:
                for atom in entry.get("receptorAtoms", []):
                    res_name = atom.get("resName", "")
                    res_id = atom.get("resID", "")
                    chain = atom.get("chain", "")
                    if res_name and res_id:
                        residue_str = f"{chain}:{res_name}{res_id}"
                        receptor_residue_summary[interaction_name].add(residue_str)

        residue_rows = []
        for interaction_type, residues in receptor_residue_summary.items():
            for res in sorted(residues):
                residue_rows.append({
                    "interaction_type": interaction_type,
                    "receptor_residue": res
                })

        residue_df = pd.DataFrame(residue_rows)
        
        # Save the results with timestamp for better organization
        output_csv_path = os.path.join(output_dir, 'output_resid.csv')
        residue_df.to_csv(output_csv_path, index=False)
        
        print(f"✅ Analysis completed successfully!")
        print(f"📊 Generated {len(residue_rows)} interaction records")
        print(f"📁 Results saved to: {output_csv_path}")
        print(f"📁 Full BINANA output in: {output_dir}")
        
else:
    print("❌ BINANA analysis failed. Please check the error messages above.")
