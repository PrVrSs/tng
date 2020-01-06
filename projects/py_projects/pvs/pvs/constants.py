"""Constants"""
import os
import pathlib
import typing
from enum import Enum, auto

import immutables


class Quality(Enum):
    LD = auto()  # 240p
    NHD = auto()  # 360p
    SD = auto()  # 480p
    ED = auto()  # 480p 60 fps
    HD = auto()  # HD 720p
    HD_60_FPS = auto()  # HD 720p 60 fps
    FULL_HD = auto()  # Full HD 1080p
    FULL_HD_60_FPS = auto()  # Full HD 1080p 60 fps
    UHD = auto()  # 4k
    UHD_60_FPS = auto()  # 4k 60 fps


class Rendition(typing.NamedTuple):
    resolution: str
    bitrate_low_motion: int
    bitrate_high_motion: int
    audio_bitrate: int


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = pathlib.Path(__file__).parent


RENDITIONS = {
    Quality.LD: Rendition(resolution='426x240', bitrate_low_motion=400, bitrate_high_motion=600, audio_bitrate=64),
    Quality.NHD: Rendition(resolution='640x360', bitrate_low_motion=700, bitrate_high_motion=900, audio_bitrate=96),
    Quality.SD: Rendition(resolution='854x480', bitrate_low_motion=1250, bitrate_high_motion=1600, audio_bitrate=128),
    Quality.ED: Rendition(resolution='854x480', bitrate_low_motion=1250, bitrate_high_motion=1600, audio_bitrate=128),
    Quality.HD: Rendition(resolution='1280x720', bitrate_low_motion=2500, bitrate_high_motion=3200, audio_bitrate=128),
    Quality.HD_60_FPS: Rendition(resolution='1280x720', bitrate_low_motion=3500, bitrate_high_motion=4400, audio_bitrate=128),
    Quality.FULL_HD: Rendition(resolution='1920x1080', bitrate_low_motion=4500, bitrate_high_motion=5300, audio_bitrate=192),
    Quality.FULL_HD_60_FPS: Rendition(resolution='1920x1080', bitrate_low_motion=5800, bitrate_high_motion=7400, audio_bitrate=192),
    Quality.UHD: Rendition(resolution='3840x2160', bitrate_low_motion=14000, bitrate_high_motion=18200, audio_bitrate=192),
    Quality.UHD_60_FPS: Rendition(resolution='3840x2160', bitrate_low_motion=23000, bitrate_high_motion=29500, audio_bitrate=192),
}

MIME_TYPE = immutables.Map(
    M4S='video/iso.segment',
    MP4='video/mp4',
    M4A='audio/mp4',
    MPD='application/dash+xml',
)
