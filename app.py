"""Flask App Project."""

from flask import Flask, jsonify, Response, request
# import uvicorn, aiohttp, asyncio
# from io import BytesIO
from fastai.vision.all import *



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

learn = setup_learner()

app = Flask(__name__)

@app.route('/')
def index():
    html = path / 'view' / 'index.html'
    return Response(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze():
    print("appel fct analyse")
    data = await request.file()
    img_bytes = await (data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction, _, values = learn.predict(img)
    label = str(prediction)
    accuracy = values[int(prediction)].item()
    return Response({'result': label + ' ({:05.2f}%)'.format(accuracy * 100)})

if __name__ == '__main__':
    app.run()
