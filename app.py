"""Flask App Project."""

from flask import Flask, jsonify, Response
# import uvicorn, aiohttp, asyncio
# from io import BytesIO
from fastai.vision.all import *

app = Flask(__name__)

path = Path(__file__).parent

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_file_url, model_path/model_file_name)
    learn = load_learner(model_path / model_file_name)
    return learn



@app.route('/')
def index():
    html = path / 'view' / 'index.html'
    return Response(html.open().read())


if __name__ == '__main__':
    app.run()
