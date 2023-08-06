"""
Utilities from processing, converting, and transforming videos
TODO: 
- Remove reliance on ffmpeg_streaming
"""
# ///////////////////
# Imports
# ///////////////////
from typing import Optional, Dict, Any, Tuple

from ffmpeg_streaming import FFProbe

import dada_audio
from dada_log import DadaLogger
from dada_errors import RequestError
from dada_utils import path, etc

# ///////////////////
# Doc Strings
# ///////////////////


FILEPATH_PARAM = ":param filepath: The input file for this function."


# ///////////////////
# Logger
# ///////////////////

log = DadaLogger(name="dada-video-ffmpeg-utils")


# ///////////////////
# FFPROBE FUNCTIONS
# ///////////////////


def ffprobe_get_all_data(filepath: str) -> Dict[str, Any]:
    f"""
    Get data about a video file via ffprobe.
    {FILEPATH_PARAM}
    :return dict
    """
    return FFProbe(filepath).all()


def ffprobe_get_fields(
    filepath: str, prefix: str = "ffp", defaults: Dict[str, Any] = {}, **kwargs
) -> Dict[str, Any]:
    f"""
    Get fields for filepath via ffprobe
    {FILEPATH_PARAM}
    :param prefix: a string to prefix all field names with
    :param defaults: defaults to pass into the function.
    :return dict
    """
    #  FFPROBE OUTPUT:
    #     {'streams': [
    #         {
    #         'index': 0,
    #         'codec_name': 'h264',
    #         'codec_long_name': 'H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10',
    #         'profile': 'High',
    #         'codec_type': 'video',
    #         'codec_time_base': '1001/60000',
    #         'codec_tag_string': 'avc1',
    #         'codec_tag': '0x31637661',
    #         'width': 1920,
    #         'height': 1080,
    #         'coded_width': 1920,
    #         'coded_height': 1088,
    #         'has_b_frames': 1,
    #         'sample_aspect_ratio': '1:1',
    #         'display_aspect_ratio': '16:9',
    #         'pix_fmt': 'yuv420p',
    #         'level': 40,
    #         'color_range': 'tv',
    #         'color_space': 'bt709',
    #         'color_transfer': 'bt709',
    #         'color_primaries': 'bt709',
    #         'chroma_location': 'left',
    #         'refs': 1,
    #         'is_avc': 'true',
    #         'nal_length_size': '4',
    #         'r_frame_rate': '30000/1001',
    #         'avg_frame_rate': '30000/1001',
    #         'time_base': '1/30000',
    #         'start_pts': 0,
    #         'start_time': '0.000000',
    #         'duration_ts': 123030,
    #         'duration': '4.101000',
    #         'bit_rate': '5756481',
    #         'bits_per_raw_sample': '8',
    #         'nb_frames': '126',
    #     },
    #     'disposition': {
    #         'default': 1,
    #         'dub': 0,
    #         'original': 0,
    #         'comment': 0,
    #         'lyrics': 0,
    #         'karaoke': 0,
    #         'forced': 0,
    #         'hearing_impaired': 0,
    #         'visual_impaired': 0,
    #         'clean_effects': 0,
    #         'attached_pic': 0,
    #         'timed_thumbnails': 0
    #     },
    #     'tags': {
    #         'creation_time': '2020-04-05T03:55:57.000000Z',
    #         'language': 'und',
    #         'handler_name': 'Core Media Video'
    #         }
    #     },
    #     {
    #     'index': 1,
    #     'codec_long_name': 'AAC (Advanced Audio Coding)',
    #     'profile': 'LC',
    #     'codec_type': 'audio',
    #     'codec_time_base': '1/44100',
    #     'codec_tag_string': 'mp4a',
    #     'codec_tag': '0x6134706d',
    #     'sample_fmt': 'fltp',
    #     'sample_rate': '44100',
    #     'channels': 2,
    #     'channel_layout': 'stereo',
    #     'bits_per_sample': 0,
    #     'r_frame_rate': '0/0',
    #     'avg_frame_rate': '0/0',
    #     'time_base': '1/44100',
    #     'start_pts': 0,
    #     'start_time': '0.000000',
    #     'duration_ts': 180854,
    #     'duration': '4.100998',
    #     'bit_rate': '127914',
    #     'max_bit_rate': '127999',
    #     'nb_frames': '180',
    #     'disposition': {'default': 1,
    #         'dub': 0,
    #         'original': 0,
    #         'comment': 0,
    #         'lyrics': 0,
    #         'karaoke': 0,
    #         'forced': 0,
    #         'hearing_impaired': 0,
    #         'visual_impaired': 0,
    #         'clean_effects': 0,
    #         'attached_pic': 0,
    #         'timed_thumbnails': 0},
    #     'tags': {
    #         'creation_time': '2020-04-05T03:55:57.000000Z',
    #         'language': 'und',
    #         'handler_name': 'Core Media Audio'}}],
    #     'format': {'filepath': 'dada/config/assets/video/vortex.mp4',
    #     'nb_streams': 2,
    #     'nb_programs': 0,
    #     'format_name': 'mov,mp4,m4a,3gp,3g2,mj2',
    #     'format_long_name': 'QuickTime / MOV',
    #     'start_time': '0.000000',
    #     'duration': '4.101000',
    #     'size': '3095455',
    #     'bit_rate': '6038439',
    #     'probe_score': 100,
    #     'tags': {'major_brand': 'mp42',
    #     'minor_version': '1',
    #     'compatible_brands': 'mp41mp42isom',
    #     'creation_time': '2020-04-05T03:55:57.000000Z'}}}
    # """
    if not path.exists(filepath):
        raise RequestError(f"Video file `{filepath}` does not exist")

    # fun ffprobe
    raw_data = ffprobe_get_all_data(filepath)

    # build up the list of fields: toplevel information
    ffp_format = raw_data.get("format", {})
    fields = {
        "probe_score": ffp_format.get("probe_scode", None),
        "format_name": ffp_format.get("format_long_name", None),
        "created_date": ffp_format.get("tags", {}).get("creation_time"),
    }

    # split the audio /video streams and add suffix for multi-video / multi-audio stream files
    (
        vid,
        aud,
        num_video_streams,
        num_audio_streams,
    ) = _split_ffprobe_video_and_audio_streams(raw_data.get("streams", []))

    fields.update(
        {
            "has_audio": num_audio_streams >= 1,
            "num_audio_streams": num_audio_streams,
            "has_video": num_video_streams >= 1,
            "num_video_streams": num_video_streams,
        }
    )

    # get video fields
    if fields["has_video"]:
        fields.update(_get_ffprobe_video_fields(vid, num_video_streams))

    # get audio fields
    if fields["has_audio"]:
        fields.update(_get_ffprobe_audio_fields(aud, num_audio_streams))

    # get id3 tags
    fields.update(
        {
            f"audio_id3_{k}": v
            for k, v in dada_audio.id3_tags_to_fields(ffp_format.get("tags", {}))
        }
    )

    # prefix keys and return non-null data
    return etc.get_fields_data(fields, prefix, defaults)


def _split_ffprobe_video_and_audio_streams(
    streams: list,
) -> Tuple[dict, dict, int, int]:
    # split the streams and namesspace values by stream number
    # only take one audio and one video stream
    # return: Tuple[video, audio, num_video_streams, num_audio_streams]
    aud = {}
    vid = {}
    num_audio_streams = 0
    num_video_streams = 0
    for stream in streams:
        if stream.get("codec_type") == "video":
            num_video_streams += 1
            if num_video_streams == 1:
                vid.update(stream)
            else:
                vid.update({f"{k}_{num_video_streams}": v for k, v in stream.items()})
        elif stream.get("codec_type") == "audio":
            num_audio_streams += 1
            if num_audio_streams == 1:
                aud.update(stream)
            else:
                aud.update({f"{k}_{num_audio_streams}": v for k, v in stream.items()})
    return vid, aud, num_video_streams, num_audio_streams


def _get_ffprobe_video_fields(vid: dict, num_video_streams: int) -> dict:
    # build up per-stream video attributes
    fields = {}

    # build up per-stream video attributes
    for i in range(1, num_video_streams + 1):

        #  create field suffix
        suffix = ""
        if i > 1:
            suffix = f"_{i}"

        fields.update(
            {
                f"video_codec_name{suffix}": vid.get(f"codec_name{suffix}", None),
                f"video_color_range{suffix}": vid.get(f"color_range{suffix}", None),
                f"video_width{suffix}": vid.get(f"width{suffix}", None),
                f"video_height{suffix}": vid.get(f"height{suffix}", None),
                f"video_level{suffix}": vid.get(f"level{suffix}", None),
                f"video_bit_rate{suffix}": vid.get(f"bit_rate{suffix}", None),
                f"video_duration{suffix}": vid.get(f"duration{suffix}", None),
                f"video_start_time{suffix}": vid.get(f"start_time{suffix}", None),
                f"video_num_frames{suffix}": vid.get(f"nb_frames", 0),
            }
        )

        # add frame rate as calculation
        # '30000/1001',
        fr = vid.get(f"avg_frame_rate{suffix}", None)
        if fr:
            parts = fr.split("/")
            if len(parts) >= 2:
                fr = float(parts[0].strip()) / float(parts[1].strip())
            else:
                log.debug(f"Invalid ffmpg field avg_frame_rate: {fr}")
                fr = None
        fields[f"avg_frame_rate{suffix}"] = fr

        # add sample aspect ratio as x/y data
        for k in ["sample_aspect_ratio", "display_aspect_ratio"]:
            parts = vid.get(f"{k}{suffix}", "").split(":")
            if not len(parts) >= 2:
                log.debug(f"Invalid ffmpg field {k}: {vid.get(k)}")
                continue
            fields[f"{k}_x{suffix}"] = int(parts[0].strip())
            fields[f"{k}_y{suffix}"] = int(parts[1].strip())
    return fields


def _get_ffprobe_audio_fields(aud, num_audio_streams) -> dict:
    # build up per-stream video attributes
    fields = {}
    for i in range(1, num_audio_streams + 1):

        #  create field suffix
        suffix = ""
        if i > 1:
            suffix = f"_{i}"

        fields.update(
            {
                f"audio_codec_name{suffix}": aud.get(f"codec_name{suffix}", None),
                f"audio_is_stereo{suffix}": int(aud.get(f"channels{suffix}", 1)) == 2,
                f"audio_sample_rate{suffix}": aud.get(f"sample_rate{suffix}", None),
                f"audio_bit_rate{suffix}": aud.get(f"bit_rate{suffix}", None),
                f"audio_num_frames{suffix}": aud.get(f"nb_frames{suffix}", None),
            }
        )

        # audio dispositions
        for name, value in aud.get(f"disposition{suffix}", {}).items():
            fields[f"audio_disposition_is_{name}{suffix}"] = int(value) == 1
    return fields


# ///////////////////
# FFMPEG FUNCTIONS
# ///////////////////


def ffmpeg_get_frame(
    filepath: str, out_filepath: Optional[str] = None, start: str = "00:00:00.000"
) -> str:
    f"""
    Get a frame of a video. You can use this function to generate a default thumbnail for a video.
    {FILEPATH_PARAM}
    :param out_filepath: an optional output filepath (with 'png' or 'jpeg' extension)
    :param frame_num: the frame number to fetch (from the start)
    :return str
    """
    if not out_filepath:
        out_filepath = path.get_tempfile(ext="png")
    command = f"ffmpeg -i '{filepath}' -ss {start} -vframes 1 '{out_filepath}'"
    process = path.exec(command)
    if not process.ok:
        raise RequestError(
            f"command `{command}` failed because of:{'*'*60}`{process.stderr or process.stdout}`{'*'*60}"
        )
    if not path.exists(out_filepath):
        raise RequestError(
            f" command `{command}` did not successfully create file: '{out_filepath}'"
        )
    return out_filepath


def ffmpeg_get_first_frame(filepath: str, out_filepath: Optional[str] = None) -> str:
    f"""
    Get the first frame of a video. You can use this function to generate a default thumbnail for a video.
    {FILEPATH_PARAM}
    :param out_filepath: an optional output filepath (with 'png' or 'jpeg' extension)
    :return str
    """
    return ffmpeg_get_frame(filepath, out_filepath, start="00:00:00.000")
