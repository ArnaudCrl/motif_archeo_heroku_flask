"""Flask App Project."""

from flask import Flask, jsonify, Response
# import uvicorn, aiohttp, asyncio
# from io import BytesIO
from fastai.vision.all import *

app = Flask(__name__)
path = Path(__file__).parent

@app.route('/')
def index():
    html = path / 'view' / 'index.html'
    return Response(html.open().read())


if __name__ == '__main__':
    app.run()
