import os
import ffmpeg
from config import VIDEOS_DIR, AUDIO_DIR, VIDEO_WIDTH, VIDEO_HEIGHT


def process_video(input_path, audio_file, output_filename, caption=None):
    """
    Resize to vertical 9:16, merge audio, optionally add caption.
    Returns path to processed output file.
    """
    output_path = os.path.join(VIDEOS_DIR, output_filename)
    audio_path = os.path.join(AUDIO_DIR, audio_file)

    video = ffmpeg.input(input_path)

    # Scale and pad to 1080x1920 (vertical)
    video = video.filter(
        "scale",
        w=VIDEO_WIDTH,
        h=VIDEO_HEIGHT,
        force_original_aspect_ratio="decrease",
        force_divisible_by=2,
    ).filter(
        "pad",
        w=VIDEO_WIDTH,
        h=VIDEO_HEIGHT,
        x="(ow-iw)/2",
        y="(oh-ih)/2",
        color="black",
    )

    if caption:
        video = video.filter(
            "drawtext",
            text=caption,
            fontsize=40,
            fontcolor="white",
            x="(w-text_w)/2",
            y="h-100",
            box=1,
            boxcolor="black@0.5",
            boxborderw=10,
        )

    if os.path.exists(audio_path):
        audio = ffmpeg.input(audio_path)
        out = ffmpeg.output(
            video,
            audio,
            output_path,
            vcodec="libx264",
            acodec="aac",
            shortest=None,
            **{"b:a": "192k"},
        )
    else:
        out = ffmpeg.output(
            video,
            output_path,
            vcodec="libx264",
            acodec="aac",
        )

    ffmpeg.run(out, overwrite_output=True, quiet=True)
    return output_path
