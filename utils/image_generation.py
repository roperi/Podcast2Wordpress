# Copyright © 2024 roperi

import os
import requests
import base64
from dotenv import load_dotenv
from config import PROMPT_SUFFIX

# Load environment variables
load_dotenv()

# Load credentials
stability_api_key = os.getenv('STABILITY_API_KEY')
stability_api_host = os.getenv('STABILITY_API_HOST')
stability_engine_id = os.getenv('STABILITY_ENGINE_ID')


# STABILITY AI

def generate_image(filename, prompt):
    """
    Generates an image based on the given prompt and saves it locally.

    Args:
        filename (str): The name of the output image file.
        prompt (str): The text prompt for generating the image.

    Returns:
        str: The file path of the generated image.

    """
    api_host = stability_api_host
    engine_id = stability_engine_id
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {stability_api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": f"{prompt}, {PROMPT_SUFFIX}",
                    "weight": 1
                },
                {
                    "text": "(((NSFW)))",
                    "weight": -1
                }
            ],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 20,
        },
    )
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))
    # Get data
    data = response.json()
    image_base64 = data["artifacts"][0]["base64"]

    # Ensure 'output' directory exists
    if not os.path.exists('output'):
        os.makedirs('output')

    # Save locally
    image_filename = f"output/{filename}.png"
    with open(image_filename, "wb") as f:
        f.write(base64.b64decode(image_base64))

    return image_filename
