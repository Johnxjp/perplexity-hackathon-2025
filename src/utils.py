import os
import requests


def download_image_file(url: str, dest_path: str) -> None:
    """
    Downloads an image file from a URL to a destination path
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }  # Add header so wikipedia and other sites won't block.
    response = requests.get(url, stream=True, headers=headers)
    if response.status_code == 200:
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
    else:
        print(f"Failed to download image from {url}, status code: {response.status_code}")
