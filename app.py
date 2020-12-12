from io import BytesIO
from flask import Flask, request, render_template, flash, redirect, url_for
import os
from PIL import Image
from random import choice
from werkzeug.utils import secure_filename
from flask import send_from_directory


UPLOAD_FOLDER = 'downloads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = "temp." + file.filename.split(".")[-1]
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            path = "static/images/Vignettes/"
            # print(os.listdir(path))
            prediction = [choice(os.listdir(path)),
                          choice(os.listdir(path)),
                          choice(os.listdir(path))]
            probas = ["90.12%", "7.54%", "2.14%"]

            result1 = []
            result2 = []
            result3 = []

            for f in os.listdir(path + prediction[0]):
                result1.append("""static/images/Vignettes/{}/{}""".format(prediction[0], f))

            for f in os.listdir(path + prediction[1]):
                result2.append("""static/images/Vignettes/{}/{}""".format(prediction[1], f))

            for f in os.listdir(path + prediction[2]):
                result3.append("""static/images/Vignettes/{}/{}""".format(prediction[2], f))

            return render_template('result.html', prediction=prediction, probas=probas, result1=result1,
                                   result2=result2,
                                   result3=result3)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
