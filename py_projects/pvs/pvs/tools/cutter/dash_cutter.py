import pathlib
from typing import Iterable, Tuple

from ..exec import run
from .i_cutter import ICutter


class DashCutter(ICutter):
    async def cut_file(self, input_file: str = '', output_dir: str = '', qualities: Iterable = None) -> None:
        for index in range(6):
            pathlib.Path(f'{output_dir}/{index}').mkdir(parents=True, exist_ok=True)

        sample_dash: str = f'{output_dir}/sample_dash.mp4'
        mpd: str = f'{output_dir}/index.mpd'

        cmd_sample = self._create_sample(input_file=input_file, output_file=sample_dash)
        cmd_dash = self._create_dash(input_file=sample_dash, output_file=mpd)
        await run(*cmd_sample)
        await run(*cmd_dash)

    @staticmethod
    def _create_sample(input_file: str, output_file: str) -> Tuple[str, ...]:
        return (
            'ffmpeg', '-y',
            '-i', f'{input_file}',
            '-c:v', 'libx264',
            '-x264opts', 'keyint=24:min-keyint=24:no-scenecut',
            '-r', '24',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-bf', '1',
            '-b_strategy', '0',
            '-sc_threshold', '0',
            '-pix_fmt', 'yuv420p',
            '-map', '0:v:0',
            '-map', '0:a:0',
            '-map', '0:v:0',
            '-map', '0:a:0,',
            '-map', '0:v:0',
            '-map', '0:a:0',
            '-b:v:0', '250k',
            '-filter:v:0', 'scale=-2:240',
            '-profile:v:0', 'baseline',
            '-b:v:1', '750k',
            '-filter:v:1', 'scale=-2:480',
            '-profile:v:1', 'main',
            '-b:v:2', '1500k',
            '-filter:v:2', 'scale=-2:720',
            '-profile:v:2', 'high',
            f'{output_file}',
        )

    @staticmethod
    def _create_dash(input_file: str, output_file: str) -> Tuple[str, ...]:
        return (
            'ffmpeg', '-y',  # '-re',
            '-i', f'{input_file}',
            '-map', '0',
            '-use_timeline', '1',
            # '-window_size', '5',
            '-adaptation_sets', 'id=0,streams=v id=1,streams=a',
            '-f', 'dash',
            '-init_seg_name', '$RepresentationID$/index.m4s',
            '-media_seg_name', '$RepresentationID$/$Number$.m4s',
            f'{output_file}',
        )


'''
ffmpeg -y -i 03.mp4 -c:v libx264 -x264opts "keyint=24:min-keyint=24:no-scenecut" -r 24 -c:a aac
-b:a 128k -bf 1 -b_strategy 0 -sc_threshold 0 -pix_fmt yuv420p -map 0:v:0
-map 0:a:0 -map 0:v:0 -map 0:a:0 -map 0:v:0 -map 0:a:0 -b:v:0 250k
-filter:v:0 "scale=-2:240" -profile:v:0 baseline -b:v:1 750k
-filter:v:1 "scale=-2:480" -profile:v:1 main -b:v:2 1500k -filter:v:2 "scale=-2:720" -profile:v:2 high sample_dash.mp4


ffmpeg -y -re -i sample_dash.mp4 -map 0 -use_timeline 1 -use_template 1 -window_size 2 -adaptation_sets "id=0,streams=v id=1,streams=a"
-f dash sample.mpd
'''
