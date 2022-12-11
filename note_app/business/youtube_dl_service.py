from __future__ import unicode_literals
from typing import Callable

from threading import Thread

from note_app import config
import youtube_dl


class YoutubeDlService:
    def download(self, url: str, send_message_fn: Callable[[str], None]) -> str:
        thread = Thread(target=self.download_in_thread, args=[url, send_message_fn])
        thread.start()

        return 'Скачиваю'

    def download_in_thread(self, url: str, send_message_fn: Callable[[str], None]):
        def my_hook(result):
            self._on_finish_hook(result, send_message_fn)

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'format': 'bestaudio/best',
            'progress_hooks': [my_hook],
            'outtmpl': f'{config.FILE_PATH}/%(title)s-%(id)s.%(ext)s',
            'restrictfilenames': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
            except:
                send_message_fn('Ошибка')

    @staticmethod
    def _on_finish_hook(result, send_message_fn: Callable[[str], None]):
        if result['status'] == 'finished':
            file_name = result['filename'].split('/').pop()
            send_message_fn(f'Скачано {config.WEB_FILE_PATH}/{file_name}')
