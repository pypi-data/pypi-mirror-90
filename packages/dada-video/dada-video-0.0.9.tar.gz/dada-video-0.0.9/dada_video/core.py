from typing import Union, List, Optional

from moviepy.editor import *

import dada_text
from dada_log import DadaLogger
from dada_utils import path
from dada_errors import RequestError

_log = DadaLogger(name="dada-video")

# core methods #


def load(filepath) -> VideoFileClip:
    """
    Load a moviepy VideoFileClip object given a filepath
    """
    return VideoFileClip(filepath)


def get_subclip(
    clip: VideoFileClip, start: Union[int, float], end: Union[int, float]
) -> VideoFileClip:
    """
    Get a sub clip of a video.
    """
    return clip.subclip(start, end)


def resize(clip: VideoFileClip, **kwargs):
    """
    Resize a clip. If passing in width and height, aspect ratio will be modified.
    if only one parameter is passed in, the aspect ratio will be mantained.
    """

    c_w = clip.w
    c_h = clip.h

    # don't increase the size of a clip
    if kwargs.get("height", 0) >= c_h:
        kwargs["height"] = c_h

    if kwargs.get("width", 0) >= c_h:
        kwargs["width"] = c_h

    return clip.fx(vfx.resize, **kwargs)


def write(clip: VideoFileClip, filepath: str, **kwargs) -> None:
    """
    Write a clip to video file
    https://zulko.github.io/moviepy/getting_started/videoclips.html#exporting-video-clips
    """
    return clip.write_videofile(filepath, **kwargs)  # default codec: 'libx264', 24 fps


def write_gif(clip: VideoFileClip, filepath: str, **kwargs) -> None:
    """
    Write clip to gif file
    https://zulko.github.io/moviepy/getting_started/videoclips.html#exporting-video-clips
    """
    return clip.write_gif(filepath, **kwargs)


def write_img(clip: VideoFileClip, filepath: str, **kwargs) -> None:
    """
    Write clip to gif file
    https://zulko.github.io/moviepy/getting_started/videoclips.html#exporting-video-clips
    """
    return clip.save_frame(filepath, **kwargs)


# special methods #


def get_chunks(
    clip: VideoFileClip, max_duration: Union[int, float] = 60, buffer: float = 0.001
) -> List[VideoFileClip]:
    """
    Given a max duration (default 60 seconds) split a clip up into a list of clips
    """
    dur = clip.duration
    # if clip is too short, do nothing
    if dur <= max_duration:
        return [clip]

    # otherwise split up clip into chunks

    # generate start and end positions
    clip_starts = [c for c in range(0, int(dur), max_duration)]
    clip_ends = [c + max_duration - buffer for c in clip_starts]
    clip_ends[-1] = dur  # ensure final clip gets to the end.

    # chunk into clips
    clip_chunks = []
    for start, end in zip(clip_starts, clip_ends):
        clip_chunks.append(get_subclip(clip, start, end))
    return clip_chunks


def process_chunks(
    filepath,
    out_filepath: Optional[str] = None,
    max_duration: Union[int, float] = 60,
    resize_opts: dict = {"width": 640},
    write_opts: dict = {"fps": 24, "audio": False},
    slugify: bool = True,
    overwrite: bool = True,
) -> List[str]:
    """
    Write a video file into a list of chunked files.
    """

    clip = load(filepath)
    clip = resize(clip, **resize_opts)

    if not out_filepath:
        ext = path.get_ext(filepath)
        out_filepath = filepath.replace(f".{ext}", "-{i}." + ext)
        _log.debug(f"automatically generated chunk fp pattern: {out_filepath}")

    if r"{i}" not in out_filepath:
        raise RequestError(
            "out_filepath must contain a string {i} in order to format successive chunks"
        )

    out_filepaths = []
    for i, clip in enumerate(get_chunks(clip, max_duration=max_duration), start=1):
        out_fp = out_filepath.format(i=i)
        if slugify:
            d = path.get_dir(out_fp)
            n = path.get_name(out_fp)
            e = path.get_ext(out_fp)
            out_fp = path.join(d, f"{dada_text.get_slug(n)}.{e}")
        _log.debug(f"Writing chunk {i} to file: {out_fp}")

        if not path.exists(out_fp) or overwrite:
            # remove audio optionally
            if not write_opts.get("audio", False):
                clip = clip.without_audio()

            write(clip, out_fp, **write_opts)

        out_filepaths.append(out_fp)
    return out_filepaths
