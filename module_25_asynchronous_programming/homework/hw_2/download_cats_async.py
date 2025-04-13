import asyncio
from pathlib import Path

import aiohttp


async def download_cat(session: aiohttp.ClientSession, idx: int, out_path: Path):
    async with session.get('https://cataas.com/cat') as response:
        content = await response.read()
        file_path = out_path / f"{idx}.png"
        await asyncio.to_thread(_sync_write, file_path, content)


def _sync_write(file_path: Path, content: bytes):
    with open(file_path, 'wb') as f:
        f.write(content)


async def download_all_cats(count: int, out_path: Path):
    out_path.mkdir(exist_ok=True, parents=True)
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as session:
        tasks = [download_cat(session, i, out_path) for i in range(count)]
        await asyncio.gather(*tasks)


def run_async(count: int, out_path: Path):
    asyncio.run(download_all_cats(count, out_path))
