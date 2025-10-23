# Introduction

BINANA (BINding ANAlyzer) is a python-implemented algorithm for analyzing ligand
binding. The program identifies key binding characteristics like hydrogen bonds,
salt bridges, and pi interactions. As input, BINANA accepts receptor and ligand
files in the PDBQT (preferred) or PDB formats. PDBQT files can be generated from
the more common PDB file format using the [free converter provided with
AutoDockTools](http://mgltools.scripps.edu/downloads). As output, BINANA
identifies and describes key protein/ligand interactions.

**Note: This is a streamlined version of BINANA that contains only the Python functionality.**

# Citation

If you use BINANA in your work, please cite:

BINANA: A Novel Algorithm for Ligand-Binding Characterization. Durrant JD,
McCammon JA. J Mol Graph Model. 2011 Apr; 29(6): 888-893. doi:
10.1016/j.jmgm.2011.01.004

# License

BINANA 2.1 is released under the [Apache License, Version
2.0](https://opensource.org/licenses/Apache-2.0). 

# Modifications Made to This Version

This is a **streamlined Python-only version** of BINANA with the following modifications:

## 🗑️ Removed Components
- **JavaScript implementation** (`javascript/` directory)
- **Web application** (`web_app/` directory)
- **Example files and tutorials** (`python/example/` directory)
- **Documentation files**: `CHANGES.md`, `INTERACTIONS.md`, `CONTRIBUTING.md`, etc.
- **Development files**: `.gitignore`, `CODEOWNERS`, etc.

## ✅ Retained Components
- **Core Python functionality** (`python/binana/` package)
- **Command-line script** (`python/run_binana.py`)
- **Essential documentation** (`README.md`, `LICENSE.md`)

## 📁 Current Directory Structure

| Directory/File           | Description
|---------------------------|------------------------------------------
| `./python/`              | All Python code
| `./python/run_binana.py` | Script for command-line use
| `./python/binana/`       | Python library (e.g., `import binana`)
| `./LICENSE.md`           | Apache 2.0 License
| `./README.md`            | This documentation

# How to Use This Streamlined Version

## 🚀 Command-line Usage

### Basic Syntax
```bash
python3 /path/to/binana/python/run_binana.py -receptor <receptor.pdbqt> -ligand <ligand.pdbqt> -output_dir <output_directory>
```

### ⚠️ Important: Create Output Directory First
BINANA does **not** automatically create the output directory. You must create it manually:

```bash
# Create output directory
mkdir -p ./results/

# Run BINANA analysis
python3 /path/to/binana/python/run_binana.py \
  -receptor receptor.pdbqt \
  -ligand ligand.pdbqt \
  -output_dir ./results/
```

### Example Usage
```bash
# Navigate to your working directory
cd /path/to/your/work/

# Create results directory
mkdir -p ./binana_output/

# Run analysis
python3 /home/davis/projects/binana/python/run_binana.py \
  -receptor protein.pdbqt \
  -ligand molecule.pdbqt \
  -output_dir ./binana_output/
```

## 📊 Output Files

After successful execution, the output directory will contain:

| File                    | Description
|-------------------------|------------------------------------------
| `output.json`          | Detailed interaction data in JSON format
| `output.csv`           | Tabular interaction data
| `log.txt`              | Analysis log and parameters used
| `*.pdb`                | Visualization files for different interaction types
| `state.vmd`            | VMD visualization state file

## 🐍 Python Library Usage

You can also import BINANA as a Python library:

```python
import sys
sys.path.append('/path/to/binana/python/')
import binana

# Run analysis programmatically
args = [
    "-receptor", "receptor.pdbqt",
    "-ligand", "ligand.pdbqt",
    "-output_dir", "./output/"
]

binana.run(args)
```

## 🔧 Common Parameters

| Parameter                          | Default | Description
|------------------------------------|---------|------------------------------------------
| `-receptor`                        | -       | Receptor PDBQT file (required)
| `-ligand`                          | -       | Ligand PDBQT file (required)
| `-output_dir`                      | -       | Output directory (required)
| `-output_json`                     | -       | JSON output file path
| `-output_csv`                      | -       | CSV output file path  
| `-hydrogen_bond_dist_cutoff`       | 4.0     | H-bond distance cutoff (Å)
| `-hydrophobic_dist_cutoff`         | 4.0     | Hydrophobic contact distance (Å)
| `-pi_pi_interacting_dist_cutoff`   | 7.5     | π-π interaction distance (Å)
| `-salt_bridge_dist_cutoff`         | 5.5     | Salt bridge distance (Å)

## 🎯 Integration with Custom Scripts

This streamlined version is perfect for integration with molecular docking pipelines. Example workflow:

```python
# binding_mode_analysis.py
import subprocess
import json
import pandas as pd

def run_binana_analysis(receptor_file, ligand_file, output_dir):
    """Run BINANA analysis and return results"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run BINANA
    command = [
        "python3", "/path/to/binana/python/run_binana.py",
        "-receptor", receptor_file,
        "-ligand", ligand_file,
        "-output_dir", output_dir
    ]
    
    subprocess.run(command, check=True)
    
    # Load results
    with open(f"{output_dir}/output.json", 'r') as f:
        return json.load(f)

# Usage
results = run_binana_analysis("protein.pdbqt", "ligand.pdbqt", "./analysis/")
```

## 🛠️ Troubleshooting

### Error: "No such file or directory: './output_dir/log.txt'"
**Solution**: Create the output directory before running BINANA:
```bash
mkdir -p ./your_output_directory/
```

### Warning: "END or ENDMDL term found in ligand file"
**Explanation**: Your ligand file contains multiple poses. BINANA only analyzes the first pose.
**Solution**: This is normal behavior. If you need to analyze multiple poses separately, split the file using `vina_split`.

### Warning: "There is no atom named 'XYZ' in protein residue"
**Explanation**: The protein structure is missing some standard atoms (usually hydrogen atoms).
**Solution**: These warnings don't affect the core analysis but may reduce accuracy. Consider using a more complete protein structure if available.

### Python Import Error
**Solution**: Make sure to add the BINANA path to your Python path:
```python
import sys
sys.path.append('/path/to/binana/python/')
import binana
```

## 📞 Support

This is a streamlined version. For the full original BINANA with web interface and JavaScript support, visit:
- Original repository: [http://git.durrantlab.com/jdurrant/binana](http://git.durrantlab.com/jdurrant/binana)
- Web application: [http://durrantlab.com/binana](http://durrantlab.com/binana)