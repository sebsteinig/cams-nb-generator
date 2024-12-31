import yaml
from pathlib import Path
import argparse
from src.notebook_generator import NotebookGenerator
from src.db_utils import get_enabled_variables

def load_master_config(config_file):
    """Load master configuration file."""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description='Generate CAMS visualization notebooks')
    parser.add_argument('config', help='Path to master configuration YAML file')
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path('notebooks')
    output_dir.mkdir(exist_ok=True)
    
    # Initialize notebook generator
    generator = NotebookGenerator(output_dir=output_dir)
    
    # Load master config
    master_config = load_master_config(args.config)
    product = master_config.get('product')
    if not product:
        raise ValueError("Master config must specify a 'product' field")
    
    # Get all enabled variables for the product
    variables = get_enabled_variables(product)
    
    # Generate notebooks for each enabled variable
    for var_data in variables:
        layer_name = var_data['layers'][1]['values']['layer_name']
        description = var_data.get('description', '').replace(' ', '_')
        print(f"Generating notebook for layer {layer_name}...")
        print(f"Description: {description}")
        # Create config for this variable by combining master config with variable-specific data
        var_config = master_config.copy()
        var_config['layer'] = layer_name
        var_config['name'] = description
        
        # Update any variable-specific parameters
        if 'params' not in var_config:
            var_config['params'] = {}
        var_config['params'].update({
            'title': var_data.get('title', ''),
            'description': var_data.get('description', ''),
            'variable': layer_name
        })
        
        # Generate the notebook
        generator.generate_notebook(layer_name, var_config)

if __name__ == '__main__':
    main() 