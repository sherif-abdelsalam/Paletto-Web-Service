import os
import requests
from urllib.parse import urlparse

def download_model_if_needed():
    """Download the model file if it doesn't exist locally."""
    model_path = 'ImageRecoloring.h5'
    
    if not os.path.exists(model_path):
        print("Model file not found locally. Downloading...")
        
        # Default Google Drive URL (converted to direct download format)
        default_url = 'https://drive.usercontent.google.com/download?id=1izTApGGhx-o0I4-eShMNRupcPsEwGUty&export=download&authuser=0'
        model_url = os.environ.get('MODEL_URL', default_url)
        
        if not model_url:
            raise Exception("MODEL_URL environment variable not set and no default URL available.")
        
        try:
            response = requests.get(model_url, stream=True)
            response.raise_for_status()
            
            with open(model_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Model downloaded successfully to {model_path}")
        except Exception as e:
            raise Exception(f"Failed to download model: {str(e)}")
    else:
        print("Model file found locally.")
