import os
from typing import List

import torch
from diffusers import (
    DiffusionPipeline,
    PNDMScheduler,
    LMSDiscreteScheduler,
    DDIMScheduler,
    EulerDiscreteScheduler,
    EulerAncestralDiscreteScheduler,
    DPMSolverMultistepScheduler,
)
# from diffusers.pipelines.stable_diffusion.safety_checker import (
#     StableDiffusionSafetyChecker,
# )


MODEL_ID = "black-forest-labs/FLUX.1-schnell"
MODEL_CACHE = "diffusers-cache"


class Predictor:
    def __init__(self):
        self.pipe = None

    def setup(self):
        """Load the model into memory to make running multiple predictions efficient"""
        print("Loading pipeline...")
        common_args = {
            "torch_dtype": torch.bfloat16,
            "use_safetensors": True
        }
        self.pipe = DiffusionPipeline.from_pretrained(
            MODEL_ID,
            # safety_checker=safety_checker,
            cache_dir=MODEL_CACHE,
            local_files_only=True,
            **common_args
        ).to("cuda")

        self.pipe.vae.enable_slicing()
        self.pipe.vae.enable_tiling()
        self.pipe.enable_xformers_memory_efficient_attention()

    @torch.inference_mode()
    def predict(self, prompt, width, height, num_outputs, num_inference_steps, guidance_scale, seed):
        """Run a single prediction on the model"""
        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")

        # self.pipe.scheduler = make_scheduler(scheduler, self.pipe.scheduler.config)

        generator = torch.Generator("cuda").manual_seed(seed)
        output = self.pipe(
            prompt=[prompt] if prompt is not None else None,
            num_images_per_prompt=num_outputs,
            width=width,
            height=height,
            guidance_scale=guidance_scale,
            generator=generator,
            num_inference_steps=num_inference_steps,
        )

        output_paths = []
        for i, sample in enumerate(output.images):
            # if output.nsfw_content_detected and output.nsfw_content_detected[i] and self.NSFW:
            #     continue

            output_path = f"/tmp/out-{i}.png"
            sample.save(output_path)
            output_paths.append(output_path)

        if len(output_paths) == 0:
            raise Exception(
                f"Try running it again, or try a different prompt."
            )

        return output_paths


# def make_scheduler(name, config):
#     return {
#         "PNDM": PNDMScheduler.from_config(config),
#         "KLMS": LMSDiscreteScheduler.from_config(config),
#         "DDIM": DDIMScheduler.from_config(config),
#         "K_EULER": EulerDiscreteScheduler.from_config(config),
#         "K_EULER_ANCESTRAL": EulerAncestralDiscreteScheduler.from_config(config),
#         "DPMSolverMultistep": DPMSolverMultistepScheduler.from_config(config),
#     }[name]
