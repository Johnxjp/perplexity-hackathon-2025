from pytubefix import YouTube


def download_youtube_video(url: str, output_path: str = "./data/") -> str:
    """
    Downloads a YouTube video from the given URL to the specified output path.

    Args:
        url (str): The URL of the YouTube video.
        output_path (str): The directory where the video will be saved.

    Returns:
        str: The file path of the downloaded video.
    """
    yt = YouTube(url)
    stream = yt.streams.filter(file_extension="mp4").get_highest_resolution()
    file_path = stream.download(output_path=output_path)
    return file_path


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=_ahTP_Zn7nU"
    downloaded_file = download_youtube_video(video_url)
    print(f"Video downloaded to: {downloaded_file}")
