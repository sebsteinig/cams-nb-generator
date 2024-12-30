from pathlib import Path
import nbformat as nbf
from nbformat.v4 import new_markdown_cell, new_code_cell

class NotebookBlocks:
    def __init__(self):
        self.template_dir = Path('templates')
        self.content_dir = Path('content')
    
    def _load_file_content(self, file_path: str | Path) -> str:
        """Load content from a file, relative to content directory."""
        path = Path(file_path)
        if not path.is_absolute():
            # Try both content and template directories
            for base_dir in [self.content_dir, self.template_dir]:
                full_path = base_dir / path
                if full_path.exists():
                    return full_path.read_text()
        return path.read_text()

    def create_cell_sequence(self, cells_config: list, global_params: dict = None) -> list:
        """Create a sequence of cells from configuration."""
        notebook_cells = []
        
        for cell in cells_config:
            if isinstance(cell, str):  # Simple string format
                file_path = cell
                cell_params = {}
            elif isinstance(cell, dict):  # Dict format with potential params
                file_path = next(iter(cell))  # First key is the file path
                cell_params = cell[file_path] if cell[file_path] else {}
            else:
                raise ValueError(f"Invalid cell configuration: {cell}")

            # Determine type based on file extension
            if file_path.endswith(('.py', '.ipynb')):
                cell_type = 'code'
            elif file_path.endswith(('.md', '.txt')):
                cell_type = 'md'
            else:
                # Assume it's direct markdown content
                cell_type = 'md'
                content = self._substitute_params(file_path, global_params)
                notebook_cells.append(new_markdown_cell(content))
                continue
            
            # Load and process content
            content = self._load_file_content(file_path)
            if cell_params or global_params:
                content = self._substitute_params(content, {**global_params, **cell_params})
            
            # Create appropriate cell type
            if cell_type == 'md':
                notebook_cells.append(new_markdown_cell(content))
            elif cell_type == 'code':
                notebook_cells.append(new_code_cell(content))
        
        return notebook_cells

    def _substitute_params(self, content: str, params: dict = None) -> str:
        """Substitute parameters in content."""
        if not params:
            return content
        
        # For eccharts_metadata, just assign directly without params wrapper
        if 'eccharts_metadata.py' in content:
            return f"eccharts_metadata = {params['eccharts_metadata']}"
        
        # For other parameters, use the standard substitution
        for key, value in params.items():
            content = content.replace(f"${{{key}}}", str(value))
        
        return content

    def create_section(self, section_config: dict, global_params: dict = None) -> list:
        """Create cells for a section based on its configuration."""
        if 'cells' not in section_config:
            return []
        
        # Add section header based on name
        section_name = section_config['name']
        cells = [new_markdown_cell(f"{section_name}")]
        
        # Add remaining cells with parameters
        cells.extend(self.create_cell_sequence(section_config['cells'], global_params))
        
        return cells

    def execute_script(self, script_path, params=None):
        """
        Execute a Python script with given parameters before notebook generation.
        
        Parameters:
        -----------
        script_path : str
            Path to the Python script to execute
        params : dict, optional
            Parameters to pass to the script
        """
        try:
            path = Path(script_path)
            script_found = False
            
            # Try both content and template directories
            for base_dir in [self.content_dir, self.template_dir]:
                full_path = base_dir / path
                if full_path.exists():
                    script_found = True
                    script_path = full_path
                    break
                
            if not script_found:
                raise FileNotFoundError(f"Script not found: {script_path}")
            
            # Create a new namespace for script execution
            namespace = {}
            
            # Add parameters to namespace if provided
            if params:
                namespace.update(params)
            
            # Read and execute the script
            with open(script_path, 'r') as f:
                script_content = f.read()
                exec(script_content, namespace)
            
        except Exception as e:
            print(f"Error executing script {script_path}: {str(e)}")
            raise