#!/usr/bin/env python3
"""
Example usage of BINANA Binding Mode Analysis Toolkit

This script demonstrates different ways to use the toolkit for binding analysis.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path to import our toolkit
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from binding_analyzer import BindingAnalyzer
    from quick_analysis import analyze_binding, get_interaction_summary, find_key_residues
except ImportError as e:
    print(f"Error importing toolkit: {e}")
    print("Make sure you're running this from the binana directory")
    sys.exit(1)


def example_quick_analysis():
    """Demonstrate quick analysis functionality."""
    print("=" * 60)
    print("🚀 EXAMPLE 1: Quick Binding Analysis")
    print("=" * 60)
    
    # Example files (update these paths to your actual files)
    receptor = "test_data/receptorH.pdbqt"  # Update this path
    ligand = "test_data/ligand_1.pdbqt"     # Update this path
    
    # Check if example files exist
    if not (os.path.exists(receptor) and os.path.exists(ligand)):
        print("⚠️  Example files not found. Please update the file paths in this script.")
        print(f"Looking for: {receptor} and {ligand}")
        return
    
    try:
        # Quick analysis - returns a DataFrame
        results_df = analyze_binding(receptor, ligand, output_dir="./example_output/")
        
        print(f"📊 Found {len(results_df)} interaction records")
        print("\n🔍 First 5 interactions:")
        print(results_df.head())
        
        print(f"\n📋 Interaction types found:")
        print(results_df['interaction_type'].value_counts())
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")


def example_interaction_summary():
    """Demonstrate interaction summary functionality."""
    print("\n" + "=" * 60)
    print("📈 EXAMPLE 2: Interaction Summary")
    print("=" * 60)
    
    receptor = "test_data/receptorH.pdbqt"
    ligand = "test_data/ligand_1.pdbqt"
    
    if not (os.path.exists(receptor) and os.path.exists(ligand)):
        print("⚠️  Example files not found. Skipping this example.")
        return
    
    try:
        # Get summary statistics
        summary = get_interaction_summary(receptor, ligand)
        
        print(f"🧬 Total interactions: {summary['total_interactions']}")
        print(f"🎯 Unique residues involved: {summary['unique_residues']}")
        
        print(f"\n📋 Breakdown by interaction type:")
        for interaction_type, count in summary['interaction_breakdown'].items():
            print(f"   • {interaction_type}: {count}")
        
        print(f"\n🔑 Key binding residues:")
        key_residues = summary['key_residues'][:10]  # Show first 10
        print(f"   {', '.join(key_residues)}")
        if len(summary['key_residues']) > 10:
            print(f"   ... and {len(summary['key_residues']) - 10} more")
        
    except Exception as e:
        print(f"❌ Summary generation failed: {e}")


def example_find_specific_residues():
    """Demonstrate finding residues by interaction type."""
    print("\n" + "=" * 60)
    print("🔍 EXAMPLE 3: Find Specific Interaction Types")
    print("=" * 60)
    
    receptor = "test_data/receptorH.pdbqt"
    ligand = "test_data/ligand_1.pdbqt"
    
    if not (os.path.exists(receptor) and os.path.exists(ligand)):
        print("⚠️  Example files not found. Skipping this example.")
        return
    
    try:
        # Find different types of interactions
        interaction_types = [
            'hydrophobic_contacts',
            'hydrogen_bonds', 
            'close_contacts',
            'pi_pi_stackings'
        ]
        
        for interaction_type in interaction_types:
            residues = find_key_residues(receptor, ligand, interaction_type)
            print(f"🧪 {interaction_type}: {len(residues)} residues")
            if residues:
                print(f"   Examples: {', '.join(residues[:5])}")
                if len(residues) > 5:
                    print(f"   ... and {len(residues) - 5} more")
            else:
                print(f"   No {interaction_type} found")
            print()
        
    except Exception as e:
        print(f"❌ Specific residue search failed: {e}")


def example_full_analyzer():
    """Demonstrate full BindingAnalyzer class usage."""
    print("\n" + "=" * 60) 
    print("🔬 EXAMPLE 4: Full Analyzer Class")
    print("=" * 60)
    
    receptor = "test_data/receptorH.pdbqt"
    ligand = "test_data/ligand_1.pdbqt"
    
    if not (os.path.exists(receptor) and os.path.exists(ligand)):
        print("⚠️  Example files not found. Skipping this example.")
        return
    
    try:
        # Create analyzer with custom settings
        analyzer = BindingAnalyzer(show_output=False)  # Quiet mode
        
        # Run full analysis
        results = analyzer.analyze(
            receptor_file=receptor,
            ligand_file=ligand,
            output_dir="./full_analysis_output/",
            save_csv=True
        )
        
        print(f"📊 Analysis completed!")
        print(f"📁 Output directory: {results['output_directory']}")
        print(f"📄 CSV file: {results['csv_file']}")
        print(f"🧬 Total interactions: {len(results['residue_summary'])}")
        
        # Access the full BINANA data if needed
        full_data = results['full_binana_data']
        print(f"🗂️  Full BINANA data keys: {list(full_data.keys())[:5]}...")
        
    except Exception as e:
        print(f"❌ Full analysis failed: {e}")


def main():
    """Run all examples."""
    print("🧪 BINANA Binding Mode Analysis Toolkit - Examples")
    print("=" * 60)
    
    # Create test data directory structure
    os.makedirs("test_data", exist_ok=True)
    
    print("📝 Note: Update the file paths in this script to point to your actual PDBQT files.")
    print("Expected files:")
    print("  - test_data/receptorH.pdbqt (receptor protein)")
    print("  - test_data/ligand_1.pdbqt (ligand molecule)")
    print()
    
    # Run examples
    example_quick_analysis()
    example_interaction_summary()  
    example_find_specific_residues()
    example_full_analyzer()
    
    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("💡 Check the generated output directories for results.")
    print("=" * 60)


if __name__ == "__main__":
    main()