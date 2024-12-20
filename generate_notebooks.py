import yaml
from pathlib import Path
import argparse
from src.notebook_generator import NotebookGenerator

def load_variable_config(variable_file):
    """Load configuration for a single variable."""
    with open(variable_file, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Generate CAMS visualization notebooks')
    parser.add_argument('--variables', nargs='*', help='Specific variables to process')
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path('notebooks')
    output_dir.mkdir(exist_ok=True)
    
    # Initialize notebook generator
    generator = NotebookGenerator(output_dir=output_dir)
    
    # Get list of variable files to process
    variables_dir = Path('variables')
    if args.variables:
        variable_files = [variables_dir / f"{var}.yaml" for var in args.variables]
    else:
        variable_files = list(variables_dir.glob('*.yaml'))
    
    # Generate notebooks
    for var_file in variable_files:
        if not var_file.exists():
            print(f"Warning: Configuration file {var_file} not found")
            continue
            
        variable_id = var_file.stem
        config = load_variable_config(var_file)
        print(f"Generating notebook for {variable_id}...")
        generator.generate_notebook(variable_id, config)

if __name__ == '__main__':
    main() 