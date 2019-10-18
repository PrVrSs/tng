import os
import pathlib
from functools import reduce
from typing import Iterable, Tuple, Any, Text

from pvs.errors import CutterException
from pvs.constants import RENDITIONS

from ..exec import run, writter
from .i_cutter import ICutter


class HlsCutter(ICutter):

    def __init__(self, max_bitrate_ratio: float = 1.07, rate_monitor_buffer_ratio: float = 1.5, segment_target_duration: int = 20):
        self._max_bitrate_ratio = max_bitrate_ratio
        self._rate_monitor_buffer_ratio = rate_monitor_buffer_ratio
        self._segment_target_duration = segment_target_duration

    async def cut_file(self, input_file: str = '', output_dir: str = '', qualities: Iterable = None):
        qualities = qualities or RENDITIONS.keys()

        if not os.path.exists(input_file):
            raise CutterException(f'file {input_file} was not found!')

        renditions = (
            rendition for rendition in map(RENDITIONS.get, qualities) if rendition is not None
        )

        cmd, playlist = await self._get_command_to_create_playlist(input_file, output_dir, renditions)

        await writter(f'{output_dir}/playlist.m3u8', playlist)
        await run(*cmd)

    async def _get_command_to_create_playlist(self, input_file: str, output_file: str, renditions: Iterable) -> Tuple[Tuple, str]:
        fps = await self._get_fps(input_file)

        static_params = self._get_static_params(fps=fps, segment_target_duration=self._segment_target_duration)
        master_playlist = '#EXTM3U\n#EXT-X-VERSION:3\n'
        cmd = tuple()

        for rendition in renditions:
            resolution = rendition.resolution
            bitrate = rendition.bitrate_low_motion
            audiorate = rendition.audio_bitrate
            width, height = map(int, resolution.split('x'))
            maxrate = round(bitrate * self._max_bitrate_ratio)
            buff_size = round(bitrate * self._rate_monitor_buffer_ratio)
            bandwidth = bitrate * 1000
            name = f'{height}p'

            pathlib.Path(f'{output_file}/{name}').mkdir(parents=True, exist_ok=True)

            cmd += self._get_rendition_command(name, width, height, bitrate, maxrate, buff_size, audiorate, output_file, static_params)
            master_playlist += f'#EXT-X-STREAM-INF:BANDWIDTH={bandwidth},RESOLUTION={resolution}\n{name}/index.m3u8\n'

        return (
            'ffmpeg',
            '-hide_banner', '-y',
            '-i', input_file,
            *cmd
        ), master_playlist

    @staticmethod
    async def _get_fps(filename: str) -> int:
        args: tuple = (
            'ffprobe',
            '-v', '0',
            '-of', 'csv=p=0',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=r_frame_rate',
            filename
        )

        fps: str = await run(*args)

        if not fps:
            return 0

        return reduce(lambda x, y: round(x / y), map(int, fps.split('/')))

    @staticmethod
    def _get_static_params(fps: int, segment_target_duration: int) -> Tuple[str, ...]:
        return (
            '-c:a', 'aac',
            '-ar', '48000',
            '-c:v', 'h264',
            '-profile:v', 'main',
            '-crf', '20',
            '-sc_threshold', '0',
            '-g', f'{fps * 2}',
            '-keyint_min', f'{fps}',
            '-hls_time', f'{segment_target_duration}',
            '-hls_playlist_type', 'vod',
        )

    @staticmethod
    def _get_rendition_command(name: str,
                               width: int,
                               height: int,
                               bitrate: int,
                               max_rate: int,
                               buff_size: int,
                               audio_rate: int,
                               output_file: str,
                               static_params: Tuple = None,
                               ) -> Tuple[str, ...]:
        return (
            *static_params,
            '-vf', f'scale=w={width}:h={height}:force_original_aspect_ratio=decrease',
            '-b:v', f'{bitrate}k',
            '-maxrate', f'{max_rate}k',
            '-bufsize', f'{buff_size}k',
            '-b:a', f'{audio_rate}k',
            '-hls_segment_filename', f'{output_file}/{name}/%03d.ts', f'{output_file}/{name}/index.m3u8',
        )
