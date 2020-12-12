from io import BytesIO
from PIL import Image
import base64
from flask import Flask, request, render_template, flash, redirect, url_for
import asyncio, aiohttp
from fastai.vision.all import *
import os


UPLOAD_FOLDER = 'downloads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        
        # check if the post request has the file part
        if 'file' not in request.form:
            flash('No file part')
            return redirect(request.url)
        file = request.form['file']

        imgdata = base64.b64decode(str(file))
        with Image.open(BytesIO(imgdata)) as image:
            image.save(UPLOAD_FOLDER + 'temp.png')
        
       
        pred, pred_idx, probs = learn.predict("downloads/temp.png")
        classes = learn.dls.vocab
        predictions = sorted(zip(classes, map(float, probs)), key=lambda p: p[1], reverse=True)

#         path = "static/images/Vignettes/"
#         # print(os.listdir(path))
        prediction = [str(predictions[0][0])[4:],
                      str(predictions[1][0])[4:],
                      str(predictions[2][0])[4:]]
        print(predition)

#         probas = [str('%.2f' % (predictions[0][1] * 100)) + "%",
#                   str('%.2f' % (predictions[1][1] * 100)) + "%",
#                   str('%.2f' % (predictions[2][1] * 100)) + "%"]

#         result1 = []
#         result2 = []
#         result3 = []

#         for f in os.listdir(path + prediction[0]):
#             result1.append("""static/images/Vignettes/{}/{}""".format(prediction[0], f))

#         for f in os.listdir(path + prediction[1]):
#             result2.append("""static/images/Vignettes/{}/{}""".format(prediction[1], f))

#         for f in os.listdir(path + prediction[2]):
#             result3.append("""static/images/Vignettes/{}/{}""".format(prediction[2], f))

#         return render_template('result.html', prediction=prediction, probas=probas, result1=result1, result2=result2,
#                                result3=result3)

    return render_template('index.html')


def make_square(im, desired_size=512):
    old_size = im.size  # old_size[0] is in (width, height) format

    ratio = float(desired_size) / max(old_size)
    new_size = tuple([int(x * ratio) for x in old_size])

    im = im.resize(new_size, Image.ANTIALIAS)

    new_im = Image.new("L", (desired_size, desired_size))
    new_im.paste(im, ((desired_size - new_size[0]) // 2,
                      (desired_size - new_size[1]) // 2))

    return new_im
 

if __name__ == '__main__':
    app.run()
