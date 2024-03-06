# Copyright © 2024 roperi

import os
import json
import tiktoken
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from config import MAX_TOKENS, TEMPERATURE, LEEWAY

# Load environment variables
load_dotenv()

# Load OpenAI
client = OpenAI()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')
model = os.getenv('OPENAI_MODEL')


class TokenProcessor:
    """
    A class for processing tokens in text.

    Attributes:
        encoding: Encoding for tokenization.
    """
    def __init__(self):
        """
        Initializes the TokenProcessor class.
        """
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_token(self, text):
        """
        Counts the number of tokens in the given text.

        Parameters:
            text (str): The text to count tokens for.

        Returns:
            int: The number of tokens in the text.
        """
        num_token = len(self.encoding.encode(text))
        return num_token

    def process_transcript(self, transcript, max_tokens):
        """
        Processes the transcript by splitting it into parts based on maximum token count.

        Parameters:
            transcript (str): The transcript to process.
            max_tokens (int): The maximum number of tokens allowed for each part.

        Returns:
            list: A list of transcript parts.
        """
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000,
                                                  length_function=self.count_token,
                                                  separators=['\n\n', '\n', ' ', ''],
                                                  chunk_overlap=2)
        chunks = splitter.split_text(transcript)
        parts = []
        current_part = ""
        current_part_tokens = 0
        for chunk in chunks:
            chunk_tokens = self.count_token(chunk)
            if current_part_tokens + chunk_tokens <= max_tokens:
                current_part += chunk + " "
                current_part_tokens += chunk_tokens
            else:
                parts.append(current_part.strip())
                current_part = chunk + " "
                current_part_tokens = chunk_tokens
        if current_part:
            parts.append(current_part.strip())
        return parts


def calculate_max_messages_tokens():
    """
    Calculates the maximum number of tokens allowed for messages.

    Returns:
        int: The maximum number of tokens allowed for messages.
    """
    if model == 'gpt-4':
        max_content_length = 8192
        completion_tokens = 4096
    elif model == 'gpt-3.5-turbo':
        max_content_length = 16385
        completion_tokens = 4096
    elif model == 'gpt-4-32k':
        max_content_length = 32768
        completion_tokens = 4096
    elif model == 'gpt-4-turbo-preview':
        max_content_length = 128000
        completion_tokens = 4096
    else:
        max_content_length = 8192
        completion_tokens = 4096

    max_messages_tokens = max_content_length - completion_tokens
    max_messages_tokens -= LEEWAY

    return max_messages_tokens


def process_transcript(podcast_name, project_name, url, transcript):
    """
    Process a transcript and generate a JSON file with key information about the transcript.

    Parameters:
        podcast_name (str): Name of the podcast.
        project_name (str): Name of the project.
        url (str): The URL of the podcast.
        transcript (str): The transcript to summarize.

    Returns:
        str: The final summary of the transcript in json format.
    """
    # Initialise text processor
    token_processor = TokenProcessor()

    max_messages_tokens = calculate_max_messages_tokens()

    # Break down transcript into parts
    transcript_parts = token_processor.process_transcript(transcript, max_messages_tokens)

    previous_summary = ""

    for part in transcript_parts:
        system_content = """
        You are an expert at processing podcast transcripts. You generate json files from
        transcripts. Each json file includes the following keys: "podcast_name", "url", "keywords", "headlines", 
        "visual_imagery" and "summary".
        You will be presented with a partial transcript from a larger podcast transcript. You 
        will modify your summaries depending on the previous partial summaries. Extract 3 to 4 relevant 
        keywords and come up with a SEO-friendly headline. For visual imagery think of the visual 
        aspects of the summary and be concise with the visual description. Refer to the speakers as the guests and hosts
        of the podcast. User will provide you with an URL and the name of the podcast.
        Your ultimate goal is to provide your answer in a JSON structure like in the following example: 
        {
            "podcast_name": "Thiiird Waves",
            "url": "https://podcast.com/thiiird-waves/episode-1.mp3",
            "keywords": ["UK", "Cultural Heritage"], 
            "headline": "Cultural Heritage: The importance of representation and self-expression",
            "visual_imagery": "People of all cultural heritages.",
            "summary": "In this episode of Thiiird Waves guests, including Haark, Tribe, Daniella, 
            and Rona, share their experiences of connecting with their cultural heritage. Haark 
            discusses his project capturing Punjabi Sikhs in the UK to inspire others with similar 
            backgrounds. He emphasizes the importance of representation and self-expression. Tribe and 
            Rona talk about their Nigerian heritage, highlighting the significance of music, food, and 
            fashion in maintaining their connection to their roots. They also touch on the role of 
            social media in celebrating cultural identities. 
            Listen to the podcast here https://podcast.com/thiiird-waves/episode-1.mp3"
        }"""

        user_content = f"""
        Summarise the following partial transcript:
        ```
        {part}
        ```
        Take into account the following previous summary:
        ```
        {previous_summary}
        ``` 
        Podcast url: {url} (note: Make sure to include the URL at the end of the summary). 
        Podcast name: {podcast_name}
        """
        conversation_outline = [
            {
                "role": "system",
                "content": system_content,
            },
            {
                "role": "user",
                "content": user_content,
            },
        ]
        response = client.chat.completions.create(
            model=model,
            messages=conversation_outline,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE
        )
        # Get content
        summary = response.choices[0].message.content
        print(summary)
        previous_summary = summary

    # Final JSON summary of the whole transcript
    final_summary = previous_summary

    # Convert it to JSON
    json_content = json.loads(final_summary)

    # Save it
    with open(f"output/{project_name}.json", "w") as json_file:
        json.dump(json_content, json_file, indent=4)

    return json_content
