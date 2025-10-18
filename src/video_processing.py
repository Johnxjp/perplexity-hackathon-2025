"""Video to frames"""

import os

import cv2


def extract_frames_interval(video_path: str, output_dir: str, interval: int | None = None):
    """
    Extract frames at specific intervals (e.g., every 30 frames)

    Returns list of file paths to the saved frames and time stamps in seconds.
    Args:
        video_path (str): The path to the video file.
        output_dir (str): The directory to save the extracted frames.
        interval (int | None): The interval (in seconds) at which to extract frames. If None, extracts all frames.

    Returns:
        list path to frame
        start time float seconds
        duration float seconds
    """
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    save_count = 0
    saved_frames: list[tuple[str, float, float]] = []
    frame_rate = round(cap.get(cv2.CAP_PROP_FPS))
    total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval_frames = interval * frame_rate if interval is not None else 1

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Save only at intervals
        if interval is not None:
            if frame_count % interval_frames == 0:
                frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
                cv2.imwrite(frame_filename, frame)
                saved_frames.append((frame_filename, save_count * interval, interval))
                save_count += 1
        else:
            frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frames.append((frame_filename, frame_count / frame_rate, 1 / frame_rate))
            save_count += 1

        frame_count += 1

    cap.release()
    print(f"Saved {save_count} frames from {total_frame_count} total frames")

    return saved_frames


def overlay_image_to_video(
    image_path: str, start_time: float, duration: float, location: tuple[int, int]
) -> None:
    """
    Overlays an image into a video file. Obtains the video frames from the video_to_frames function.

    Args:
        image_path (str): The file path to the image.
        start_time (float): The start time (in seconds) for the overlay.
        duration (float): The duration (in seconds) for the overlay.
        location (tuple[int, int]): The (x, y) location to place the overlay image.

    """
    pass
