#!/usr/bin/env python3
"""
BINANA Binding Mode Analyzer
A convenient wrapper for BINANA analysis with simplified output generation.

Usage:
    python binding_analyzer.py -r receptor.pdbqt -l ligand.pdbqt -o output_dir/
    
Or as a library:
    from binding_analyzer import BindingAnalyzer
    analyzer = BindingAnalyzer()
    results = analyzer.analyze('receptor.pdbqt', 'ligand.pdbqt', 'output/')
"""

import subprocess
import json
import pandas as pd
import os
import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Union


class BindingAnalyzer:
    """A convenient wrapper for BINANA analysis with enhanced functionality."""
    
    def __init__(self, binana_path: Optional[str] = None, show_output: bool = True):
        """
        Initialize the BindingAnalyzer.
        
        Args:
            binana_path (str, optional): Path to run_binana.py. If None, uses relative path.
            show_output (bool): Whether to show detailed BINANA output during analysis.
        """
        if binana_path is None:
            # Use relative path from this file
            current_dir = Path(__file__).parent
            self.binana_path = str(current_dir / "python" / "run_binana.py")
        else:
            self.binana_path = binana_path
            
        self.show_output = show_output
        
        # Interaction type mappings from BINANA JSON keys to readable names
        self.interaction_keys = {
            "hydrogen_bonds": "hydrogenBonds",
            "salt_bridges": "saltBridges", 
            "hydrophobic_contacts": "hydrophobicContacts",
            "pi_pi_stackings": "piStackings",
            "pi_cation_interactions": "piCationInteractions",
            "metal_complexes": "metalComplexes",
            "close_contacts": "closeContacts"
        }
    
    def validate_inputs(self, receptor_file: str, ligand_file: str) -> None:
        """Validate that input files exist and are readable."""
        if not os.path.exists(receptor_file):
            raise FileNotFoundError(f"Receptor file not found: {receptor_file}")
        if not os.path.exists(ligand_file):
            raise FileNotFoundError(f"Ligand file not found: {ligand_file}")
        if not os.path.exists(self.binana_path):
            raise FileNotFoundError(f"BINANA executable not found: {self.binana_path}")
    
    def run_binana(self, receptor_file: str, ligand_file: str, output_dir: str) -> bool:
        """
        Execute BINANA analysis.
        
        Args:
            receptor_file (str): Path to receptor PDBQT file
            ligand_file (str): Path to ligand PDBQT file  
            output_dir (str): Directory to save BINANA output
            
        Returns:
            bool: True if analysis succeeded, False otherwise
        """
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Prepare command
        command = [
            "python3", self.binana_path,
            "-receptor", receptor_file,
            "-ligand", ligand_file,
            "-output_dir", output_dir,
        ]
        
        if self.show_output:
            print(f"Running BINANA analysis...")
            print(f"Command: {' '.join(command)}")
            print("=" * 60)
        
        try:
            if self.show_output:
                # Show output in real-time
                result = subprocess.run(command, check=True)
            else:
                # Run silently
                result = subprocess.run(command, check=True, capture_output=True, text=True)
            
            if self.show_output:
                print("=" * 60)
                print("✅ BINANA analysis completed successfully!")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ BINANA analysis failed: {e}")
            if hasattr(e, 'stderr') and e.stderr:
                print(f"Error details: {e.stderr}")
            return False
    
    def parse_binana_output(self, output_dir: str) -> Tuple[pd.DataFrame, Dict]:
        """
        Parse BINANA JSON output and extract interaction information.
        
        Args:
            output_dir (str): Directory containing BINANA output files
            
        Returns:
            Tuple[pd.DataFrame, Dict]: Residue interaction summary and full data
        """
        output_json_path = os.path.join(output_dir, 'output.json')
        
        if not os.path.exists(output_json_path):
            raise FileNotFoundError(f"BINANA output file not found: {output_json_path}")
        
        # Load BINANA results
        with open(output_json_path, 'r') as f:
            binana_data = json.load(f)
        
        # Extract receptor residue interactions
        receptor_residue_summary = defaultdict(set)
        
        for interaction_name, json_key in self.interaction_keys.items():
            interactions = binana_data.get(json_key, [])
            
            for entry in interactions:
                for atom in entry.get("receptorAtoms", []):
                    res_name = atom.get("resName", "")
                    res_id = atom.get("resID", "")  
                    chain = atom.get("chain", "")
                    
                    if res_name and res_id:
                        residue_str = f"{chain}:{res_name}{res_id}"
                        receptor_residue_summary[interaction_name].add(residue_str)
        
        # Convert to DataFrame
        residue_rows = []
        for interaction_type, residues in receptor_residue_summary.items():
            for res in sorted(residues):
                residue_rows.append({
                    "interaction_type": interaction_type,
                    "receptor_residue": res
                })
        
        residue_df = pd.DataFrame(residue_rows)
        
        return residue_df, binana_data
    
    def analyze(self, 
                receptor_file: str, 
                ligand_file: str, 
                output_dir: str = "./binana_analysis/",
                save_csv: bool = True) -> Dict:
        """
        Perform complete binding mode analysis.
        
        Args:
            receptor_file (str): Path to receptor PDBQT file
            ligand_file (str): Path to ligand PDBQT file
            output_dir (str): Output directory for results
            save_csv (bool): Whether to save CSV summary
            
        Returns:
            Dict: Analysis results with DataFrames and statistics
        """
        # Validate inputs
        self.validate_inputs(receptor_file, ligand_file)
        
        # Run BINANA analysis
        if not self.run_binana(receptor_file, ligand_file, output_dir):
            raise RuntimeError("BINANA analysis failed")
        
        # Parse results
        residue_df, full_data = self.parse_binana_output(output_dir)
        
        # Save CSV summary if requested
        csv_path = None
        if save_csv:
            csv_path = os.path.join(output_dir, 'binding_mode_summary.csv')
            residue_df.to_csv(csv_path, index=False)
            
        # Generate statistics
        interaction_stats = residue_df['interaction_type'].value_counts().to_dict()
        unique_residues = residue_df['receptor_residue'].nunique()
        
        results = {
            'residue_summary': residue_df,
            'full_binana_data': full_data,
            'interaction_statistics': interaction_stats,
            'unique_residues_count': unique_residues,
            'output_directory': output_dir,
            'csv_file': csv_path
        }
        
        # Print summary
        if self.show_output:
            self._print_summary(results)
        
        return results
    
    def _print_summary(self, results: Dict) -> None:
        """Print analysis summary to console."""
        print("\n" + "=" * 60)
        print("📊 BINDING MODE ANALYSIS SUMMARY")
        print("=" * 60)
        
        print(f"🧬 Total interaction records: {len(results['residue_summary'])}")
        print(f"🎯 Unique receptor residues involved: {results['unique_residues_count']}")
        
        print(f"\n📋 Interaction type breakdown:")
        for interaction_type, count in results['interaction_statistics'].items():
            print(f"   • {interaction_type}: {count}")
        
        print(f"\n📁 Results saved to: {results['output_directory']}")
        if results['csv_file']:
            print(f"📊 CSV summary: {results['csv_file']}")
        
        print("=" * 60)


def main():
    """Command-line interface for the binding analyzer."""
    parser = argparse.ArgumentParser(
        description="BINANA Binding Mode Analyzer - Analyze protein-ligand interactions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -r protein.pdbqt -l ligand.pdbqt
  %(prog)s -r receptor.pdbqt -l molecule.pdbqt -o ./analysis/ --quiet
  %(prog)s -r protein.pdbqt -l ligand.pdbqt --no-csv
        """
    )
    
    parser.add_argument('-r', '--receptor', required=True,
                      help='Receptor PDBQT file')
    parser.add_argument('-l', '--ligand', required=True,
                      help='Ligand PDBQT file')
    parser.add_argument('-o', '--output', default='./binana_analysis/',
                      help='Output directory (default: ./binana_analysis/)')
    parser.add_argument('--quiet', action='store_true',
                      help='Run in quiet mode (minimal output)')
    parser.add_argument('--no-csv', action='store_true',
                      help='Do not save CSV summary')
    parser.add_argument('--binana-path',
                      help='Custom path to run_binana.py')
    
    args = parser.parse_args()
    
    try:
        # Initialize analyzer
        analyzer = BindingAnalyzer(
            binana_path=args.binana_path,
            show_output=not args.quiet
        )
        
        # Run analysis
        results = analyzer.analyze(
            receptor_file=args.receptor,
            ligand_file=args.ligand,
            output_dir=args.output,
            save_csv=not args.no_csv
        )
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"📁 Results available in: {results['output_directory']}")
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()