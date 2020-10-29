"""Flask App Project."""

from flask import Flask, jsonify, Response, request
import asyncio, aiohttp
from io import BytesIO
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



@app.route('/upload', methods=['POST'])
def upload():
    img_bytes = request.files['file'].read()
    return predict_from_bytes(img_bytes)
    
def predict_from_bytes(img_bytes):
    pred,pred_idx,probs = learn.predict(img_bytes)
    classes = learn.dls.vocab
    predictions = sorted(zip(classes, map(float, probs)), key=lambda p: p[1], reverse=True)
    result_html1 = path/'static'/'result1.html'
    result_html2 = path/'static'/'result2.html'
    
    result_html = str(result_html1.open().read() +str(predictions[0:3]) + result_html2.open().read())
    return Response(result_html)


@app.route('/')
def index():
    index_html = path/'static'/'index.html'
    return Response(index_html.open().read())

if __name__ == '__main__':
    app.run()
