import json
import tempfile
import subprocess
from pathlib import Path

def _fetch_metadata(collection: str, name: str, tmp_dir: Path) -> dict:
    """Fetch metadata from ecCharts MongoDB for a given collection and name."""
    subprocess.run([
        'bash', '-c',
        f'module load webdev && web-catalogue -s bol-prod -c {collection} -d {tmp_dir} -a dump {name}'
    ])
    
    json_path = Path(tmp_dir) / collection / 'tmp' / f'{name}.json'
    with open(json_path) as f:
        return json.load(f)

def get_enabled_variables(product: str) -> list:
    """Get all enabled variables for a given product from MongoDB.
    
    Args:
        product: The product name to query
        
    Returns:
        List of dictionaries containing variable metadata for enabled variables
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Fetch all variables for the product
        subprocess.run([
            'bash', '-c',
            f'module load webdev && web-catalogue -s bol-prod -p {product} -d {tmp_dir} -a dump'
        ])
        
        # Get all JSON files in the product directory
        product_dir = Path(tmp_dir) / 'product' / product
        enabled_vars = []
        
        for json_file in product_dir.glob('*.json'):
            with open(json_file) as f:
                var_data = json.load(f)
                if var_data.get('enabled', False):
                    enabled_vars.append(var_data)
        
        return enabled_vars

def get_variable_metadata(layer_name: str) -> dict:
    """Get combined layer and style metadata from MongoDB."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Get layer and style metadata
        layer_metadata = _fetch_metadata('layer', layer_name, tmp_dir)
        style_metadata = _fetch_metadata('style', layer_metadata['style'], tmp_dir)
        
        # Extract and convert levels to floats
        levels = [float(x) for x in style_metadata['data']['contour']['contour_level_list'].split('/')]
        
        # Convert RGB strings to tuples of floats
        colours = [
            tuple(float(x) for x in rgb.strip('rgb()').split(','))
            for rgb in style_metadata['data']['contour']['contour_shade_colour_list'].split('/')
        ]
        
        # Combine relevant metadata
        return {
            'layer_name': layer_name,
            'title': layer_metadata.get('title', ''),
            'description': layer_metadata.get('description', ''),
            'style_name': layer_metadata['style'],
            'levels': levels,
            'colours': colours
        }