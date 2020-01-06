from pvs.constants import BASE_DIR
from pvs.handlers.base import ok
from pvs.handlers.channel import ChannelHandler


async def handle_request(request):
    return ok()


def setup_routes(app):
    channel_handler = ChannelHandler()

    app.router.add_get('/', handle_request)
    app.router.add_get('/channels', channel_handler.handle_channels, name='channels')
    app.router.add_get('/{stream_type}/channels/{channel_id}', channel_handler.handle_channel, name='channel')
    app.router.add_get('/{stream_type}/channels/{digest}/{quality}/{file_name}', channel_handler.handle_channel_program, name='segment')

    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=f'{BASE_DIR}/static',
                          name='static')
