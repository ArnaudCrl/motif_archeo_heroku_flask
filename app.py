"""Flask App Project."""

from flask import Flask, jsonify, Response, request, render_template
import asyncio, aiohttp
from io import BytesIO
import base64
from flask_jsglue import JSGlue
from fastai.vision.all import *
from PIL import Image
import os

path = Path(__file__).parent

model_file_url = 'https://www.dropbox.com/s/swydgx4eaxj3h4h/archeo_bw.pkl?dl=1'
model_file_name = 'archeo_bw.pkl'
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
print("before app def")
app = Flask(__name__)



@app.route('/upload', methods=["POST", "GET"])
def analyse():
    img = request.args.get('img').replace(" ", "+")
    # print(img)

    with BytesIO(base64.b64decode(img)) as img_bytes:
        im = Image.open(img_bytes)
        im = make_square(im)
        im.save("tmp" + '.jpg', 'JPEG', quality=100)
        pred, pred_idx, probs = learn.predict("tmp.jpg")
        classes = learn.dls.vocab
        predictions = sorted(zip(classes, map(float, probs)), key=lambda p: p[1], reverse=True)

        path = "static/images/Vignettes/"
        # print(os.listdir(path))
        prediction = [str(predictions[0][0])[4:],
                      str(predictions[1][0])[4:],
                      str(predictions[2][0])[4:]]

        probas = [str('%.2f' % (predictions[0][1] * 100)) + "%",
                  str('%.2f' % (predictions[1][1] * 100)) + "%",
                  str('%.2f' % (predictions[2][1] * 100)) + "%"]

        result1 = []
        result2 = []
        result3 = []

        for f in os.listdir(path + prediction[0]):
            result1.append("""static/images/Vignettes/{}/{}""".format(prediction[0], f))

        for f in os.listdir(path + prediction[1]):
            result2.append("""static/images/Vignettes/{}/{}""".format(prediction[1], f))

        for f in os.listdir(path + prediction[2]):
            result3.append("""static/images/Vignettes/{}/{}""".format(prediction[2], f))

        return render_template('result.html', prediction=prediction, probas=probas, result1=result1, result2=result2,
                               result3=result3)

def make_square(im, desired_size=512):
    old_size = im.size  # old_size[0] is in (width, height) format

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    im = im.resize(new_size, Image.ANTIALIAS)

    new_im = Image.new("L", (desired_size, desired_size))
    new_im.paste(im, ((desired_size - new_size[0]) // 2,
                      (desired_size - new_size[1]) // 2))

    return new_im
 

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
