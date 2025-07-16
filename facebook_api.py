# facebook_api.py

import requests  # Used for sending HTTP requests to Facebook's Graph API
from typing import Optional  # For optional type hinting
from config import ACCESS_TOKEN, PAGE_ID  # Importing access token and page ID from a config file

def post_to_facebook(message: str, media_path: Optional[str] = None, media_type: str = "text") -> Optional[dict]:
    """
    Posts content to a Facebook Page using the Graph API.

    Depending on the `media_type`, the function can post:
    - A plain text message to the page feed.
    - An image (photo) with an optional caption (message).
    - A video with an optional caption (message).

    Args:
        message (str): The message or caption to include in the post.
        media_path (Optional[str]): Path to the media file (image or video) to be uploaded. Required if media_type is "image" or "video".
        media_type (str): The type of content to post. Should be one of "text", "image", or "video".

    Returns:
        Optional[dict]: The response from the Facebook API if the post is successful, otherwise None.
    """

    # Base URL for the Graph API request, starting with the page ID
    url = f"https://graph.facebook.com/{PAGE_ID}"

    # Query parameters for the POST request, including access token and message
    params = {
        'access_token': ACCESS_TOKEN,
        'message': message
    }

    # Used to store files when uploading image or video
    files = None

    try:
        # Handle posting an image
        if media_type == "image" and media_path:
            url += "/photos"  # Append '/photos' to the endpoint for image upload
            with open(media_path, 'rb') as f:
                # Open the image file in binary read mode and attach it to the request
                files = {'source': f}
                response = requests.post(url, params=params, files=files)

        # Handle posting a video
        elif media_type == "video" and media_path:
            url += "/videos"  # Append '/videos' to the endpoint for video upload
            with open(media_path, 'rb') as f:
                # Open the video file in binary read mode and attach it to the request
                files = {'source': f}
                response = requests.post(url, params=params, files=files)

        # Handle posting plain text (no media)
        else:
            url += "/feed"  # Append '/feed' to the endpoint for text-only posts
            response = requests.post(url, params=params)

        # Raise an exception for HTTP error responses (status codes 4xx or 5xx)
        response.raise_for_status()

        # Print and return the parsed JSON response from the Facebook API
        print("Facebook API response:", response.json())
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        # Handles HTTP-specific errors and prints the error along with response text
        print(f"HTTP error: {http_err} - {response.text}")

    except Exception as e:
        # Handles all other types of exceptions
        print(f"Error posting to Facebook: {e}")

    # Return None if the post was unsuccessful
    return None
