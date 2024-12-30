import requests
from datetime import datetime, timedelta
from pathlib import Path
import json

def download_webchart(output_dir, valid_time=None, base_time=None):
    """
    Download a webchart from ECMWF's OpenCharts API and save to file
    
    Parameters:
    -----------
    output_dir : str or Path
        Directory to save the webchart image
    valid_time : str, optional
        Forecast valid time in ISO format (YYYY-mm-ddTHH:00:00Z)
    base_time : str, optional
        Forecast base time in ISO format (YYYY-mm-ddTHH:00:00Z)
    """
    # Create output directory if it doesn't exist
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # API endpoint
    url = "https://charts.ecmwf.int/opencharts-api/v1/products/aerosol-forecasts/"
    print(f"Requesting metadata from: {url}")
    
    # Set default times if not provided
    if not valid_time or not base_time:
        now = datetime.utcnow()
        # Round to nearest hour and set minutes/seconds to 00
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = now - timedelta(days=1)
        valid_time = now.strftime("%Y-%m-%dT%H:00:00Z")
        base_time = yesterday.strftime("%Y-%m-%dT%H:00:00Z")
    
    # Parameters for the request
    params = {
        'valid_time': valid_time,
        'base_time': base_time
    }
    
    print(f"Request parameters: {params}")
    
    # Make the initial request to get the image URL
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        try:
            data = response.json()
            image_url = data['data']['link']['href']
            print(f"Found image URL: {image_url}")
            
            # Download the actual image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                output_path = output_dir / "latest_webchart.png"
                output_path.write_bytes(image_response.content)
                print(f"Webchart downloaded to {output_path}")
            else:
                raise RuntimeError(f"Failed to download image: {image_response.status_code}")
        except (KeyError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to parse API response: {str(e)}")
    else:
        raise RuntimeError(f"Failed to get image URL: {response.status_code} - {response.text}")

# Always execute when the script is run (whether through __main__ or exec())
output_dir = "data/webcharts"
if 'output_dir' in locals():  # Check if parameter was passed from YAML
    output_dir = locals()['output_dir']
download_webchart(output_dir)