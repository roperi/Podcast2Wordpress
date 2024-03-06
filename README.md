https://github.com/roperi/Podcast2Wordpress/assets/9901508/95777c6b-7445-4fe5-850e-62543cb0ac2e


<h1 align="center">Podcast2Wordpress - Easily Turn Your Podcast Episodes into WordPress Blog Posts</h1>
<h2 align="center">Deepgram + ChatGPT + Stable Diffusion + WordPress XLM-RPC</h2>


Podcast2Wordpress is a Python script designed to streamline the process of converting podcast episodes into engaging blog posts on WordPress. This tool automates the transcription of audio files, processes the transcribed content, generates visually appealing imagery, and uploads the resulting blog post to a WordPress site. 

With Podcast2Wordpress, content creators can effortlessly repurpose their podcast episodes into written blog posts, enhancing their online presence and audience engagement.

----------

## Features

- Podcast transcription from an URL 
- Generates transcription summary
- Generates a featured image from the transcription summary
- Uploads summary and image to Wordpress

## Functionality
Podcast2Wordpress performs the following tasks:
- Transcribes the audio from the provided URL.
- Processes the transcript to generate content for the blog post.
- Generates an image based on the transcript content.
- Uploads the blog post to WordPress.


## Requirements

- Python >=3.10
- Audio transcription: Deepgram API key (free)
- Transcription processing: OpenAI API key (from 5 dollars)
- Image generation: StabilityAI API Key (free)

## Tested Environment

This program has been tested and verified to work correctly in Python 3.10 Debian 10. While it may work in newer versions of Python 3.10.

## Installation

1. **Create Virtual Environment:** It's recommended to create a virtual environment to isolate the dependencies of this project. You can create a virtual environment with Python 3.10 using the following command:

    ```bash
    python3 -m venv venv
    ```

    This command will create a virtual environment named `venv` in the current directory.

2. **Activate Virtual Environment:** After creating the virtual environment, activate it using the appropriate command for your operating system:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```
      
3. **Clone the repository:**
   
    ```
    git clone https://github.com/roperi/Podcast2Wordpress.git
    ```

4. **Navigate to the project directory:**
   
    ```
    cd Podcast2Wordpress/
    ```

5. **Install the required dependencies:**
   
    ```
    pip install -r requirements.txt
    ```

## Environment file

Create a `.env` file in project folder and paste all your own API keys and related values for each key. 

Example:

```commandline
# .env

OPENAI_API_KEY="sk-abc123"
OPENAI_MODEL='gpt-3.5-turbo'
WORDPRESS_APP_PASSWORD="myS3cR3tP455W0rD"
WORDPRESS_USERNAME="podcaster"
WORDPRESS_URL="https://MyAwesomeBlog.wordpress.com/xmlrpc.php"
STABILITY_API_KEY="sk-xyz890"
STABILITY_API_HOST='https://api.stability.ai'
STABILITY_ENGINE_ID="stable-diffusion-v1-6"
DG_API_KEY='jg5sfg597sfgj75gj59sfgj58fgj5fs52c4mc'
```

### OpenAI

1. `OPENAI_API_KEY="sk-abc123"`:
   - This is the API key used to authenticate requests to the OpenAI API.
   - You can get your API from https://openai.com
   - It provides access to OpenAI's services, including language models like GPT-3.5 Turbo.
   - You should keep this key secure and avoid sharing it publicly.

2. `OPENAI_MODEL='gpt-3.5-turbo'`:
   - This specifies the model you want to use from OpenAI's offerings.
   - In this case, it's set to use the GPT-3.5 Turbo model, which is a variant of the GPT-3.5 model optimized for faster response times.
   - Podcast2Wordpress accepts: 
     - gpt-4: 8192 tokens max context window (including completion tokens)
     - gpt-3.5-turbo: 16385 max context window (including completion tokens)
     - gpt-4-32k: 32768 max context window (including completion tokens)
     - gpt-4-turbo-preview: 128000 context window (including completion tokens)

### WordPress
Any type of WordPress account (even the free ones) can get a "WordPress Application Password". Get it from your security settings in [https://wordpress.com/me/security/two-step](https://wordpress.com/me/security/two-step).  Requires activating Two-step authentication. 


1. `WORDPRESS_APP_PASSWORD="myS3cR3tP455W0rD"`:
   - Also called Wordpress Application Password. 
   - This is the password used to authenticate with the WordPress XML-RPC API.
   - It's used to allow your application to interact with WordPress programmatically, such as creating posts or managing content.

2. `WORDPRESS_USERNAME="podcaster"`:
   - This is your normal WordPress username.

3. `WORDPRESS_URL="https://MyAwesomeBlog.wordpress.com/xmlrpc.php"`:
   - This is the URL endpoint for the WordPress XML-RPC API. It has to have the `xmlrpc.php` ending.
   - It specifies the location where your application can send requests to interact with your WordPress site programmatically.

### Stability AI (DreamStudio)
As of March 2024 new DreamStudio accounts get 25 credits for free which can be used to generate ~150 images. If you haven't already, sign up for a Deepgram account or log in to your existing account [here](https://www.dreamstudio.ai/).

1. `STABILITY_API_KEY="sk-xyz890"`:
   - This is the API key used to authenticate requests to the Stability AI API.
   - Similar to the OpenAI API key, you should keep this key secure and avoid sharing it publicly.

2. `STABILITY_API_HOST='https://api.stability.ai'`:
   - This specifies the host endpoint for the Stability AI API.
   - It indicates the base URL where your application should send requests to interact with Stability AI's services.

3. `STABILITY_ENGINE_ID="stable-diffusion-v1-6"`:
   - This is the identifier for the Stability AI text to image model you want to use for image generation.
   - It specifies the specific model or version within the Stability AI system that your requests will be processed by.

### Deepgram

As of March 2024 new accounts get $200 in credit (up to 45,000 minutes), absolutely free. No credit card needed. 
If you haven't already, sign up for a Deepgram account or log in to your existing account [here](https://www.deepgram.com/).

1. `"DG_API_KEY='ad8a0ds090dads0987612csc99q83csa"`:
   - This is the API key used to authenticate requests to the DeepGram API.
   - Similar to the OpenAI API key or the Stability AI key, you should keep this key secure and avoid sharing it publicly.


## Usage

Run the script using the following command:

```
python Podcast2Wordpress.py -n "project_name" -p "podcast_name" -u "audio_file_url"`
```

Exaple:

```commandline
python Podcast2Wordpress.py -p "Thiiird Waves" \
-n "Poetry as a second language" \
-u "https://sphinx.acast.com/p/open/s/5f15a641303772024a62b7b5/e/626670f41fbc660017ed1bbc/media.mp3"
```

## Configuration

### Logging

Create a `config.py` in the project folder and paste the following:

```python
# config.py

from deepgram import DeepgramClientOptions
import logging

# Configure logging settings
config = DeepgramClientOptions(
    verbose=logging.SPAM,
    # Add other logging parameters as needed
)

# AUDIO TRANSCRIPTION
TIMEOUT_SECONDS = 1000.0

# TRANSCRIP PROCESSING
# Max content length token limit is 4096 for gpt-3.5-X and gpt-4-X
MAX_TOKENS = 4096
# Add some leeway for system content and summaries
LEEWAY = 500
# What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random,
# while lower values like 0.2 will make it more focused and deterministic.
TEMPERATURE = 0.2

# IMAGE GENERATION
PROMPT_SUFFIX = 'in an abstract art style for a blog'
```

With this configuration file you can control logging, Deepgram's timeout (especially important if you get `write operation timed out` errors), and OpenAI chat completion parameters.

## General Logging
The script logs various events and errors to a log file located in the `log` directory. Additionally, log messages are printed to the console for real-time monitoring.

## Handling Errors and Tracking Failed Audio Transcriptions


The Audio Transcriptor module within Podcast2Wordpress handles error logging for failed audio transcription attempts. If an error occurs during the transcription process, the write_to_errored_file function writes the name of the project to the audio-transcription-errored.txt file located in the output directory. This file serves as a log of projects that encountered errors during transcription, allowing for easier tracking and troubleshooting of transcription issues.

----------

## Copyright 
Copyright © 2024 roperi. 


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
