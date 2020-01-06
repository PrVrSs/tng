import pytest

from pvs.__main__ import init_app
from pvs.constants import BASE_DIR


@pytest.fixture
async def client(loop, aiohttp_client, db):
    app = init_app(config_file=f'{BASE_DIR}/pvs/config.ini', deployment_environment='test')

    return await aiohttp_client(app)


@pytest.fixture(scope='module')
def db():
    yield
