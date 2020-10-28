"""Flask App Project."""

from flask import Flask, jsonify, Response, request
import asyncio
# from io import BytesIO
from fastai.vision.all import *

path = Path(__file__).parent

model_file_url = 'https://www.dropbox.com/s/js3a84uh0dv7qit/model.pkl?dl=1'
model_file_name = 'model.pkl'
model_path = path

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(model_file_url, model_path/model_file_name)
    learn = load_learner(model_path / model_file_name)
    print("learner loaded !")
    return learn

learn = asyncio.run(setup_learner())

app = Flask(__name__)

@app.route('/')
def index():
    html = path / 'view' / 'index.html'
    return Response(html.open().read())

@app.route('/analyze', methods=['POST'])
def analyze():
    print("appel fct analyse")
    data = request.file()
    img_bytes = data['file'].read()
    img = open_image(BytesIO(img_bytes))
    prediction, _, values = learn.predict(img)
    label = str(prediction)
    accuracy = values[int(prediction)].item()
    return Response({'result': label + ' ({:05.2f}%)'.format(accuracy * 100)})

if __name__ == '__main__':
    app.run()
