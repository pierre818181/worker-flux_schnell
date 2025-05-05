INPUT_SCHEMA = {
    'prompt': {
        'type': str,
        'required': True
    },
    'width': {
        'type': int,
        'required': False,
        'default': 1024,
    },
    'height': {
        'type': int,
        'required': False,
        'default': 1024,
    },
    'num_outputs': {
        'type': int,
        'required': False,
        'default': 1,
        'constraints': lambda num_outputs: 10 > num_outputs > 0
    },
    'num_inference_steps': {
        'type': int,
        'required': False,
        'default': 50,
        'constraints': lambda num_inference_steps: 0 < num_inference_steps < 200
    },
    'guidance_scale': {
        'type': float,
        'required': False,
        'default': 7.5,
        'constraints': lambda guidance_scale: 0 < guidance_scale < 20
    },
    'seed': {
        'type': int,
        'required': False,
        'default': None
    }
}
