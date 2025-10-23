"""
Quick Binding Analysis - Simple interface for BINANA binding mode analysis

This module provides simple functions for common binding analysis tasks.
"""

from .binding_analyzer import BindingAnalyzer
import pandas as pd
from typing import Dict, Optional


def analyze_binding(receptor_file: str, 
                   ligand_file: str, 
                   output_dir: str = "./analysis/",
                   quiet: bool = False) -> pd.DataFrame:
    """
    Quick binding mode analysis with minimal setup.
    
    Args:
        receptor_file (str): Path to receptor PDBQT file
        ligand_file (str): Path to ligand PDBQT file  
        output_dir (str): Output directory
        quiet (bool): Run in quiet mode
        
    Returns:
        pd.DataFrame: Summary of receptor residue interactions
        
    Example:
        >>> results = analyze_binding('protein.pdbqt', 'ligand.pdbqt')
        >>> print(results.head())
    """
    analyzer = BindingAnalyzer(show_output=not quiet)
    results = analyzer.analyze(receptor_file, ligand_file, output_dir)
    return results['residue_summary']


def get_interaction_summary(receptor_file: str, 
                          ligand_file: str,
                          quiet: bool = True) -> Dict:
    """
    Get a quick statistical summary of interactions.
    
    Args:
        receptor_file (str): Path to receptor PDBQT file
        ligand_file (str): Path to ligand PDBQT file
        quiet (bool): Run in quiet mode (default True for summary)
        
    Returns:
        Dict: Statistics about interactions
        
    Example:
        >>> stats = get_interaction_summary('protein.pdbqt', 'ligand.pdbqt')
        >>> print(f"Found {stats['total_interactions']} interactions")
    """
    analyzer = BindingAnalyzer(show_output=not quiet)
    results = analyzer.analyze(receptor_file, ligand_file, save_csv=False)
    
    return {
        'total_interactions': len(results['residue_summary']),
        'unique_residues': results['unique_residues_count'],
        'interaction_breakdown': results['interaction_statistics'],
        'key_residues': results['residue_summary']['receptor_residue'].unique().tolist()
    }


def find_key_residues(receptor_file: str, 
                     ligand_file: str, 
                     interaction_type: Optional[str] = None,
                     quiet: bool = True) -> list:
    """
    Find key binding residues, optionally filtered by interaction type.
    
    Args:
        receptor_file (str): Path to receptor PDBQT file
        ligand_file (str): Path to ligand PDBQT file
        interaction_type (str, optional): Filter by interaction type
        quiet (bool): Run in quiet mode
        
    Returns:
        list: List of receptor residues involved in binding
        
    Example:
        >>> hydrophobic_residues = find_key_residues('protein.pdbqt', 'ligand.pdbqt', 
        ...                                        'hydrophobic_contacts')
    """
    analyzer = BindingAnalyzer(show_output=not quiet)
    results = analyzer.analyze(receptor_file, ligand_file, save_csv=False)
    
    df = results['residue_summary']
    
    if interaction_type:
        df = df[df['interaction_type'] == interaction_type]
    
    return df['receptor_residue'].unique().tolist()