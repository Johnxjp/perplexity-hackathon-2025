from typing import Tuple

from pytubefix import YouTube
import requests
from youtube_transcript_api import YouTubeTranscriptApi


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
    title = yt.title
    publish_date = yt.publish_date  # We can use for search filtering
    return file_path


def download_youtube_transcript(yt_video_id: str) -> Tuple[float, float, str]:
    """
    Downloads the transcripts of a YouTube video given its video ID.

    Args:
        yt_video_id (str): The video ID of the YouTube video. https://www.youtube.com/watch?v=_ahTP_Zn7nU -> _ahTP_Zn7nU

    Returns:
        Tuple[float, float, str]: A list of transcript segments with their start times, durations, and text. Times are in seconds.
    """
    if _is_yt_url(yt_video_id):
        yt_video_id = _extract_yt_video_id(yt_video_id)

    try:
        ytt = YouTubeTranscriptApi()
        transcripts = ytt.fetch(yt_video_id)
        return [
            (float(segment.start), float(segment.duration), _clean_transcript_text(segment.text))
            for segment in transcripts.snippets
        ]
    except Exception as e:
        print(f"Error downloading transcripts for {yt_video_id}: {e}")
        return []


def _is_yt_url(url: str) -> bool:
    """
    Checks if a given URL is a YouTube URL.

    Args:
        url (str): The URL to check.
    Returns:
        bool: True if the URL is a YouTube URL, False otherwise.
    """
    return "youtube.com" in url or "youtu.be" in url


def _extract_yt_video_id(url: str) -> str:
    """
    Extracts the YouTube video ID from a given URL.

    Args:
        url (str): The URL of the YouTube video.
    Returns:
    """
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return ""


def _clean_transcript_text(text: str) -> str:
    """
    Cleans the transcript text by removing unwanted characters or formatting.

    Args:
        text (str): The transcript text to clean.

    Returns:
        str: The cleaned transcript text.
    """
    # Remove any unwanted characters or formatting
    text = text.replace("\xa0\n", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("  ", " ")
    return text.strip()


def is_valid_url(url: str) -> bool:
    """
    Validates if a given string is a valid URL.

    Args:
        url (str): The URL string to validate.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        return False

    try:
        response = requests.get(url)
        print("RESPONSE", response)
        return response.status_code == 200
    except requests.RequestException:
        return False
