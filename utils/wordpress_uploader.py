# Copyright © 2024 roperi

import os
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load credentials
wordpress_url = os.getenv("WORDPRESS_URL")
wordpress_username = os.getenv('WORDPRESS_USERNAME')
wordpress_password = os.getenv("WORDPRESS_APP_PASSWORD")


def upload_blogpost(content, image_file_path):
    """
    Uploads a blog post to a WordPress site along with an associated image.

    Args:
        content (dict): The content of the blog post.
        image_file_path (str): The file path of the image to be uploaded.

    Returns:
        None
    """
    # Create client
    wp = Client(
        wordpress_url,
        wordpress_username,
        wordpress_password
    )

    # Parse content
    title = content.get('headline')
    blog_content = content.get('summary')
    tags = content.get('keywords')

    # Upload post
    post = WordPressPost()

    post.title = title
    post.content = blog_content
    post.terms_names = {
        'post_tag': tags,
        'category': ['News']
    }
    # Let's Now Check How To Upload Media Files
    data = {
        'name': f'{os.path.basename(image_file_path)}.png',
        'type': 'image/png'  # Media Type
    }
    # Now We Have To Read Image From Our Local Directory !
    with open(image_file_path, 'rb') as img:
        data['bits'] = xmlrpc_client.Binary(img.read())
        response = wp.call(media.UploadFile(data))

    attachment_id = response['id']

    # Above Code Just Uploads The Image To Our Gallery
    # For Adding It In Our Main Post We Need To Save Attachment ID
    post.thumbnail = attachment_id
    post.post_status = 'publish'
    post.id = wp.call(posts.NewPost(post))
