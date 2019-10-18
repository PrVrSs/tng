from aiohttp import web


def cor_headers() -> dict:
    return {
        "Access-Control-Allow-Origin": "*",
    }


async def handle_preflight(request):
    return web.Response()


def create_cors_middleware(overrides: dict = None):

    @web.middleware
    async def middleware_handler(request, handler):
        if request.method == "OPTIONS":
            response = await handle_preflight(request)
        else:
            response = await handler(request)

        response.headers.update(cor_headers())
        return response

    return middleware_handler
