# Copyright © 2024 roperi

import os
import json
import httpx
from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
)
from dotenv import load_dotenv
from config import config, TIMEOUT_SECONDS

# Load environment variables
load_dotenv()

# Load credentials
DG_API_KEY = os.getenv("DG_API_KEY")


def audio_transcriptor(url, project_name):
    """
    Process audio from a URL.

    Parameters:
        url (str): URL to an audio file.
        project_name (str): Name of the project.
    """
    try:
        # Create the 'output' folder if it doesn't exist
        if not os.path.exists('output'):
            os.makedirs('output')

        print('Initialising...')
        deepgram = DeepgramClient(DG_API_KEY, config)

        # Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            diarize=True,
            summarize="v2",
            detect_topics=False,
        )

        timeout = httpx.Timeout(TIMEOUT_SECONDS, connect=10.0)

        print(f'Transcribing `{url}`')
        audio_url = {
            'url': url
        }

        # Input is a URL
        response = deepgram.listen.prerecorded.v("1").transcribe_url(audio_url, options, timeout=timeout)
        response_dict = response.to_dict()
        print('Saving transcription...')
        output_filename = f"{project_name}__transcription.json"

        output_json = os.path.join('output', output_filename)
        with open(output_json, "w") as json_file:
            json.dump(response_dict, json_file, indent=4)

        # Process transcript text file
        print('Getting diarize from transcript...')
        return process_transcript(output_json, project_name)

    except Exception as e:
        print(f"Exception: {e}")
        write_to_errored_file(project_name)


def write_to_errored_file(project_name):
    """
    Write the project name to the errored.txt file.
    """
    errored_file_path = "output/audio-transcription-errored.txt"

    # Check if the file exists, create it if it doesn't
    if not os.path.exists(errored_file_path):
        with open(errored_file_path, "w") as errored_file:
            pass  # Create an empty file

    # Append the project name to the file
    with open(errored_file_path, "a") as errored_file:
        errored_file.write(project_name + "\n")


def process_transcript(output_json, project_name):
    """
    Process a transcript from the JSON output of Deepgram's transcription.

    Parameters:
        output_json (str): Path to the JSON file containing the transcription output.
        project_name (str): Name of the project.

    Returns:
        bool: Whether  transcript processing succeed or failed.
    """
    try:
        with open(output_json, "r") as file:
            data = json.load(file)

        # Extract paragraphs from JSON
        paragraphs_transcript = data.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get(
            'paragraphs', {}).get('transcript', "")

        # Write paragraphs to file
        with open(os.path.join('output', f'{project_name}__paragraphs.txt'), 'w') as f_paragraphs:
            f_paragraphs.write(paragraphs_transcript)

        print('Audio transcription finalised')
        return True

    except Exception as e:
        print(f"Audio Transcription failed: {str(e)}")
        return False
