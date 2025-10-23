"""
BINANA Binding Mode Analysis Toolkit

A convenient Python package for analyzing protein-ligand binding interactions
using BINANA with enhanced usability and output formatting.

Classes:
    BindingAnalyzer: Main analysis class with full functionality
    
Functions:
    analyze_binding: Quick binding analysis
    get_interaction_summary: Get interaction statistics  
    find_key_residues: Find binding residues by interaction type

Example Usage:
    
    # Method 1: Quick analysis
    from binana_toolkit import analyze_binding
    results = analyze_binding('protein.pdbqt', 'ligand.pdbqt')
    
    # Method 2: Full analysis with custom options
    from binana_toolkit import BindingAnalyzer
    analyzer = BindingAnalyzer(show_output=False)
    results = analyzer.analyze('protein.pdbqt', 'ligand.pdbqt')
    
    # Method 3: Command line
    python binding_analyzer.py -r protein.pdbqt -l ligand.pdbqt -o ./results/
"""

from .binding_analyzer import BindingAnalyzer
from .quick_analysis import analyze_binding, get_interaction_summary, find_key_residues

# Version information
__version__ = "1.0.0"
__author__ = "BINANA Toolkit Team"

# Export main classes and functions
__all__ = [
    'BindingAnalyzer',
    'analyze_binding', 
    'get_interaction_summary',
    'find_key_residues'
]