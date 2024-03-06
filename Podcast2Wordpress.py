# Copyright © 2024 roperi

import os
import sys
import argparse
import time
import logging
from utils.audio_transcription import audio_transcriptor
from utils.transcript_processor import process_transcript
from utils.image_generation import generate_image
from utils.wordpress_uploader import upload_blogpost


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Get paths
scriptdir = os.path.dirname(os.path.abspath(__file__))
mypath = os.path.join(scriptdir, 'log', 'Podcast2Wordpress.log')
# Create file handler which logs even DEBUG messages
fh = logging.FileHandler(mypath)
fh.setLevel(logging.DEBUG)
# Create console handler
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('[%(levelname)s. %(name)s, (line #%(lineno)d) - %(asctime)s] %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)


# Functions

def upload_blogpost_with_retry(content, image_file_path, max_retries=5, retry_interval=5):
    """
    Uploads a blog post to a WordPress site along with an associated image, with retry logic.

    Args:
        content (dict): The content of the blog post.
        image_file_path (str): The file path of the image to be uploaded.
        max_retries (int): Maximum number of retries. Default is 5.
        retry_interval (int): Time interval between retries in seconds. Default is 5.

    Returns:
        None
    """
    retry_count = 0
    while retry_count < max_retries:
        try:
            upload_blogpost(content, image_file_path)
            # If upload is successful, break out of the loop
            break
        except Exception as e:
            print(f"Error occurred: {e}")
            print(f"Retrying upload... (Attempt {retry_count + 1}/{max_retries})")
            retry_count += 1
            time.sleep(retry_interval)
    else:
        print(f"Upload failed after {max_retries} attempts.")


# MAIN PROGRAM

def main(url, project_name, podcast_name):
    """
    Main function to process audio transcription, generate content, and upload a blog post to WordPress.

    Args:
        url (str): The URL of the audio file.
        project_name (str): Name of the project.
        podcast_name (str): Name of the podcast.

    Returns:
        None
    """
    logger.info("Launching Podcast2Wordpress...")
    logger.info('')

    try:
        # Get audio transcription from URL
        logger.info(f'    Getting audio transcription for `{project_name}`...')
        transcribed_audio = audio_transcriptor(url, project_name)

        if transcribed_audio:
            filename = os.path.join('output', f'{project_name}__paragraphs.txt')
            with open(filename, 'r') as f:
                transcript = f.read()

            # Process transcription
            logger.info('    Processing transcript...')
            json_content = process_transcript(podcast_name, project_name, url, transcript)
            logger.debug(json_content)

            # Generate image
            txt2img_prompt = json_content.get('visual_imagery')
            logger.info(f'    Generating image from prompt: `{txt2img_prompt}`...')
            image_file_path = generate_image(project_name, txt2img_prompt)

            # Upload blogpost
            logger.info('    Uploading blogpost...')
            upload_blogpost_with_retry(json_content, image_file_path)

            logger.info(f'Done with `{project_name}`')
            logger.info('')
        else:
            logger.error(f'Failed to process audio for `{project_name}` transcription')

    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process transcripts from audio files or URLs.')
    parser.add_argument('--name', '-n', required=True, help='Name of the project.')
    parser.add_argument('--podcast', '-p', required=True, help='Name of the podcast.')
    parser.add_argument('--url', '-u', nargs=1, required=True, help='Audio file URL.')

    args = parser.parse_args()

    # Extract the podcast name and URL from the arguments
    project_name_ = args.name
    podcast_name_ = args.podcast
    url_ = args.url[0]

    # Call the main function with the URL, project name, and podcast name
    main(url_, project_name_, podcast_name_)
