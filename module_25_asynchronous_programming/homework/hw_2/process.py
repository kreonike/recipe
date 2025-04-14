import concurrent.futures
from pathlib import Path

import requests


def download_cat_process(idx: int, out_path: Path):
    response = requests.get('https://cataas.com/cat', timeout=15)
    file_path = out_path / f'{idx}.png'
    with open(file_path, 'wb') as f:
        f.write(response.content)


def run_processes(count: int, out_path: Path):
    out_path.mkdir(exist_ok=True, parents=True)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(download_cat_process, i, out_path) for i in range(count)
        ]
        concurrent.futures.wait(futures)
