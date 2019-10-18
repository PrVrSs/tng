import asyncio
import hashlib
import pathlib
from datetime import datetime

import aiofiles as aiof

from pvs.db.base import Base, DB
from pvs.db.models import (
    Program,
    Channel,
    Scheduled,
    Source
)
from pvs.constants import Quality, BASE_DIR
from pvs.tools.cutter.cutter_factory import CutterFactory, CutterType


async def create_digest(input_file: str, chunk_size: int):
    digest = hashlib.sha256()

    async with aiof.open(input_file, mode='rb') as media_file:
        while True:
            chunk = await media_file.read()

            if not chunk:
                break

            digest.update(chunk)

    return digest.hexdigest()


async def create_program(input_file: str, output_dir: str, chunk_size: int) -> Program:
    digest = await create_digest(input_file, chunk_size)

    factory = CutterFactory()
    cutter = factory.create(key=CutterType.DASH)

    pathlib.Path(f'{output_dir}/{digest}').mkdir(parents=True, exist_ok=True)

    # await cutter.cut_file(input_file=input_file, output_dir=f'{output_dir}/{digest}', qualities=(Quality.LD, ))
    await cutter.cut_file(input_file=input_file, output_dir=f'{output_dir}/{digest}', qualities=(Quality.LD,))

    return Program(digest=digest)


async def init_db(session):
    program_1 = await create_program(input_file=f'../../media/short.mp4', output_dir='../../media/dash', chunk_size=10)
    # program_2 = await create_program(input_file=f'../../../media/03.avi', output_dir='../../../media', chunk_size=100)
    # program_3 = await create_program(input_file=f'../../../media/03.avi', output_dir='../../../media', chunk_size=100)

    program_source_1 = Source(id=1, program=program_1, url=f'{BASE_DIR}/epg/media/03.avi')
    # program_source_2 = Source(id=2, program=program_2, url=f'{BASE_DIR}/epg/media/m1-1-1000000/frag-1.ts')
    # program_source_3 = Source(id=3, program=program_3, url=f'{BASE_DIR}/epg/media/m2-1-1000000/frag-2.ts')

    channel_1 = Channel(name='qwe')

    scheduled_1 = Scheduled(
        channel=channel_1,
        program=program_1,
        start_time=datetime(2019, 3, 9, 1, 17, 8, 349358),
        end_time=datetime(2019, 3, 9, 1, 18, 8, 349358)
    )

    # scheduled_2 = Scheduled(
    #     channel=channel_1,
    #     program=program_2,
    #     start_time=datetime(2019, 3, 9, 1, 19, 8, 349358),
    #     end_time=datetime(2019, 3, 9, 1, 20, 8, 349358)
    # )

    # scheduled_3 = Scheduled(
    #     channel=channel_1,
    #     program=program_3,
    #     start_time=datetime(2019, 3, 9, 1, 21, 8, 349358),
    #     end_time=datetime(2019, 3, 9, 1, 22, 8, 349358)
    # )

    session.add(program_1)
    # session.add(program_2)
    # session.add(program_3)

    session.add(program_source_1)
    # session.add(program_source_2)
    # session.add(program_source_3)

    session.add(channel_1)

    session.add(scheduled_1)
    # session.add(scheduled_2)
    # session.add(scheduled_3)

    session.commit()
    session.close()


async def main():
    DB.setup('sqlite:///../../epg/some.db')
    Base.metadata.create_all(DB.engine)
    session = DB.session()
    await init_db(session)


if __name__ == '__main__':
    asyncio.run(main())
