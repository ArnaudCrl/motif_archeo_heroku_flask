import aiohttp
from pathlib import Path
import asyncio


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)


model_file_url = 'https://www.dropbox.com/s/qjo5edcvoaif7mn/torch_resnet_model.pt?dl=1'
model_file_name = 'torch_resnet_model.pt'
asyncio.run(download_file(model_file_url, Path(model_file_name)))