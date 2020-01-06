import os
import signal
import subprocess
from app.interfaces import Plugin


class AppStarter(Plugin):

    def __init__(self):
        self._local_app: dict = {}
        self._remove_app: dict = {}

    def launch_app(self, settings: dict = None):
        settings = settings or {}
        launch_type: str = settings.get('launch_type')
        if launch_type == 'local':
            self.launch_local_app(settings)
        else:
            self.launch_remove_app()

    def launch_local_app(self, settings: dict = None):
        settings = settings or {}

        cmd = settings.get('process')

        if cmd is None:
            return

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            shell=True,
            preexec_fn=os.setsid
        )

        self._local_app[settings.get('name')] = {
            'process': process
        }

    def kill_process(self, process_name: str = '', process_type: str = ''):
        process = self._get_process(process_name, process_type)

        if process.poll():
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            return True

        return False

    def launch_remove_app(self):
        """
        :return:
        """

    def _get_process(self, process_name: str = '', process_type: str = ''):
        if process_type == 'local':
            process_opt: dict = self._local_app.get(process_name)
        else:
            process_opt: dict = self._remove_app.get(process_name)

        if process_opt is None:
            return

        return process_opt.process
