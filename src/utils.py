import os

from pytubefix import YouTube
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


def download_youtube_video(url: str, output_path: str = "./data/", resolution: str = "720p") -> str:
    """
    Downloads a YouTube video from the given URL to the specified output path.

    Args:
        url (str): The URL of the YouTube video.
        output_path (str): The directory where the video will be saved.

    Returns:
        str: The file path of the downloaded video.
    """
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension="mp4")
    stream = stream.get_by_resolution(resolution) or stream.get_highest_resolution()
    file_path = stream.download(output_path=output_path)
    return file_path
