import os
import nbformat as nbf
from .notebook_blocks import NotebookBlocks
from .db_utils import get_variable_metadata

class NotebookGenerator:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.blocks = NotebookBlocks()
    
    def generate_notebook(self, variable_id, config):
        """Generate notebook for a variable using its configuration."""
        nb = nbf.v4.new_notebook()
        
        # Extract global parameters
        global_params = config.get('params', {})
        global_params['layer_name'] = config.get('layer')
        
        # Get ecCharts metadata
        eccharts_metadata = get_variable_metadata(global_params['layer_name'])
        
        # Execute pre-execution scripts if they exist
        if 'pre_execution' in config:
            for script in config['pre_execution']:
                if isinstance(script, dict):
                    script_path = list(script.keys())[0]
                    params = list(script.values())[0]
                else:
                    script_path = script
                    params = {}

                print(f"Executing script: {script_path} with params: {params}")
                self.blocks.execute_script(script_path, params)
        
        # Add cells based on configuration
        for section in config['sections']:
            if 'cells' in section:
                # Add eccharts_metadata as a cell parameter when needed
                cells = [
                    {'python/plots/eccharts_metadata.py': {'eccharts_metadata': eccharts_metadata}} 
                    if isinstance(cell, str) and cell == 'python/plots/eccharts_metadata.py'
                    else cell
                    for cell in section['cells']
                ]
                section['cells'] = cells
            
            cells = self.blocks.create_section(section, global_params)
            nb.cells.extend(cells)
        
        # Save notebook
        output_path = self.output_dir / f"{variable_id}.ipynb"
        nbf.write(nb, output_path)