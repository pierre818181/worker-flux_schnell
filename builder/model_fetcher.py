'''
RunPod | serverless-ckpt-template | model_fetcher.py

Downloads the model from the URL passed in.
'''

import os
import requests
import torch
import json
from pathlib import Path
from diffusers import DiffusionPipeline

MODEL_CACHE = "diffusers-cache"
MODEL_URL = "https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors?download=true"
MODEL_ID = "black-forest-labs/FLUX.1-schnell"  # Keep the same model ID for compatibility with predict.py

def download_model_file(url, save_path):
    '''
    Downloads a file from the specified URL to the specified path.
    '''
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    if os.path.exists(save_path):
        print(f"Model file already exists at {save_path}")
        return
        
    print(f"Downloading model file from {url} to {save_path}")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
            print(f"Successfully downloaded model file to {save_path}")
            return
        except Exception as err:
            if attempt < max_retries - 1:
                print(f"Error encountered: {err}. Retrying attempt {attempt + 1} of {max_retries}...")
            else:
                raise

def fetch_pretrained_model(model_class, model_name, **kwargs):
    '''
    Fetches a pretrained model from the HuggingFace model hub.
    '''
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return model_class.from_pretrained(model_name, cache_dir=MODEL_CACHE, **kwargs)
        except OSError as err:
            if attempt < max_retries - 1:
                print(
                    f"Error encountered: {err}. Retrying attempt {attempt + 1} of {max_retries}...")
            else:
                raise

def get_diffusion_pipelines():
    '''
    Downloads the model file and prepares it for use with the Diffusers library.
    '''
    # Create the directory structure expected by diffusers when loading with local_files_only=True
    # The structure should mimic what would be created when downloading from HuggingFace
    model_path = Path(MODEL_CACHE) / "models--black-forest-labs--FLUX.1-schnell" / "snapshots" 
    os.makedirs(model_path, exist_ok=True)
    
    # Calculate a hash directory name to mimic diffusers pattern (simplified for this case)
    hash_dir = model_path / "main"
    os.makedirs(hash_dir, exist_ok=True)
    
    # Download the model file to the appropriate location
    model_file_path = hash_dir / "flux1-dev-fp8.safetensors"
    download_model_file(MODEL_URL, model_file_path)
    
    # Create a detailed model_index.json file to help diffusers locate the model components
    model_index = {
        "_class_name": "FluxPipeline",
        "_diffusers_version": "0.30.0.dev0",
        "scheduler": [
            "diffusers",
            "FlowMatchEulerDiscreteScheduler"
        ],
        "text_encoder": [
            "transformers",
            "CLIPTextModel"
        ],
        "text_encoder_2": [
            "transformers",
            "T5EncoderModel"
        ],
        "tokenizer": [
            "transformers",
            "CLIPTokenizer"
        ],
        "tokenizer_2": [
            "transformers",
            "T5TokenizerFast"
        ],
        "transformer": [
            "diffusers",
            "FluxTransformer2DModel"
        ],
        "vae": [
            "diffusers",
            "AutoencoderKL"
        ]
    }
    
    with open(hash_dir / "model_index.json", "w") as f:
        json.dump(model_index, f, indent=2)
    
    print("Model file downloaded and prepared for use")

if __name__ == "__main__":
    get_diffusion_pipelines()

