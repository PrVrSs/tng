import asyncio
import concurrent.futures

import youtube_dl


class YoutubeLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    @staticmethod
    def error(msg):
        print(msg)


class YTD:
    def __init__(self):
        self._ydl_opts = {
            'format': 'bestvideo+bestaudio',
            'outtmpl': '../../media/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'logger': YoutubeLogger(),
            'progress_hooks': (
                self._is_finished_hook,
            ),
        }

    def download(self, urls):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self._load_url, url): url for url in urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()
                except Exception as exc:
                    print(f'{url} generated an exception: {exc}')

    def _load_url(self, url) -> None:
        with youtube_dl.YoutubeDL(self._ydl_opts) as ydl:
            ydl.download((
                url,
            ))

    @staticmethod
    def _is_finished_hook(info: dict) -> None:
        if info.get('status') == 'finished':
            print('Done downloading, now converting ...')


async def main():
    youtube = YTD()

    youtube.download((
        # 'https://www.youtube.com/watch?v=MDGHei6Nllk',
        # 'https://www.youtube.com/watch?v=KWooB4tpQ9I'
        'https://www.youtube.com/watch?v=dpLWgntlQzw',
    ))


if __name__ == '__main__':
    asyncio.run(main())
