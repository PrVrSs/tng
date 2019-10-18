from aiohttp import web


def resp(status, **kwargs):
    rv = {
        'status': status,
    }

    rv.update(kwargs)
    return web.json_response(rv)


def ok(**kwargs):
    return resp('ok', **kwargs)
