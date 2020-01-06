import sys
import asyncio
import logging

import click
import uvloop
from aiohttp import web

from pvs.middlewares import setup_middlewares
from pvs.routes import setup_routes
from pvs.config_loader import Config
from pvs.db.base import DB


def init_app(config_file: str, deployment_environment: str) -> web.Application:
    app: web.Application = web.Application()

    Config.initialize(config_file)
    DB.setup(Config.get('DATABASE'))

    # app.on_startup.append(init_pg)
    # app.on_cleanup.append(close_pg)

    setup_routes(app)
    setup_middlewares(app)

    return app


@click.command()
@click.option('--config_file', default='pvs/config.ini', help='path to config file')
@click.option('--dev', 'deployment_environment', flag_value='DEV', default=True)
@click.option('--prod', 'deployment_environment', flag_value='PROD')
def main(config_file: str, deployment_environment: str) -> int:
    logging.basicConfig(level=logging.DEBUG)

    web.run_app(init_app(config_file, deployment_environment))

    return 0


if __name__ == '__main__':
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    sys.exit(main())  # pylint: disable=no-value-for-parameter
