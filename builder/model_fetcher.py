'''
RunPod | serverless-ckpt-template | model_fetcher.py

Downloads the model from the URL passed in.
'''

import torch
from diffusers import DiffusionPipeline

MODEL_CACHE = "diffusers-cache"
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
    Fetches the Stable Diffusion XL pipelines from the HuggingFace model hub.
    '''
    common_args = {
        "torch_dtype": torch.float8,
        "use_safetensors": True
    }

    fetch_pretrained_model(DiffusionPipeline,
                                  "black-forest-labs/FLUX.1-schnell", **common_args)
    print("Loaded MODEL")


if __name__ == "__main__":
    get_diffusion_pipelines()
