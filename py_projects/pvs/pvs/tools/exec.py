import asyncio
from typing import Any

import aiofiles as aiof


async def run(*args: Any, **kwargs: Any) -> str:
    process: Any = await asyncio.create_subprocess_exec(
        *args,
        stdin=None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout: bytes = b''
    stderr: bytes = b''

    while not process.stdout.at_eof():
        stdout += await process.stdout.readline()

    while not process.stderr.at_eof():
        stderr += await process.stderr.readline()

    await process.wait()

    if stderr:
        print(stderr)
        # raise CMDException(stderr.decode())

    return stdout.decode()


async def writter(filename: str, data) -> None:
    async with aiof.open(filename, "w") as out:
        await out.write(data)
        await out.flush()
