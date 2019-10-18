from aiohttp import web

from pvs.constants import MIME_TYPE
from pvs.handlers.base import ok
from pvs.db.base import DB
from typing import Dict, Any

from pvs.db.models import Channel, Scheduled


class ChannelHandler:
    def __init__(self):
        self._session = DB.session_factory()

    def program(self, program) -> Dict[str, Any]:
        return {
            'digest': program.digest,
        }

    def scheduled_program(self, scheduled_program) -> Dict[str, Any]:
        return {
            'start_time': scheduled_program.start_time.isoformat(' '),
            'end_time': scheduled_program.end_time.isoformat(' '),
            'program': self.program(scheduled_program.program),
        }

    def channel(self, channel: Channel, host) -> Dict[str, Any]:
        return {
            'id': channel.id,
            'name': channel.name,
            'scheduled': [
                self.scheduled_program(st) for st in self._session.query(Scheduled).filter_by(channel_id=channel.id)
            ],
            'url': '//{}/channels/{}'.format(host, channel.id)
        }

    async def handle_channels(self, request):
        self._session.query(Scheduled).filter()

        host = request.headers["Host"]
        cursor = self._session.query(Channel).order_by(Channel.name)
        channels = [self.channel(pl, host) for pl in cursor]

        return ok(channels=channels)

    async def handle_channel(self, request):

        standard_file_name = 'index.mpd'
        stream_type = request.match_info['stream_type']
        channel_id = request.match_info['channel_id']
        channel = self._session.query(Channel).filter_by(id=channel_id).first()
        scheduled = self._session.query(Scheduled).filter_by(channel=channel).first()

        filename = f'../media/{stream_type}/{scheduled.program.digest}/{standard_file_name}'

        headers = {
            'Content-Type': MIME_TYPE['MPD'],
            'Content-Disposition': "inline; filename=\"{}\"".format(filename),
        }

        return web.FileResponse(filename, headers=headers)

    async def handle_channel_program(self, request):
        stream_type = request.match_info['stream_type']
        digest = request.match_info['digest']
        quality = request.match_info['quality']
        file_count = request.match_info['file_name']

        filename = f'../media/{stream_type}/{digest}/{quality}/{file_count}'

        headers = {
            'Content-Type': MIME_TYPE['M4S'],
            'Content-Disposition': "inline; filename=\"{}\"".format(filename),
        }

        return web.FileResponse(filename, headers=headers)
