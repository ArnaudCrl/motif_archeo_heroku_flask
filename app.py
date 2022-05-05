# -*-coding:utf-8 -*

import base64
from flask import Flask, request, render_template, flash, redirect, jsonify
from pathlib import Path
from pytorch_util import *

dico = {"001-01": "https://graphbz.eu/spip.php?article6664",
        "001-02": "https://graphbz.eu/spip.php?article6665",
        "002-01": "https://graphbz.eu/spip.php?article6215",
        "002-02": "https://graphbz.eu/spip.php?article6216",
        "002-03": "https://graphbz.eu/spip.php?article6217",
        "002-04": "https://graphbz.eu/spip.php?article6218",
        "002-05": "https://graphbz.eu/spip.php?article6666",
        "003-01": "https://graphbz.eu/spip.php?article6219",
        "003-02": "https://graphbz.eu/spip.php?article6220",
        "003-03": "https://graphbz.eu/spip.php?article6221",
        "003-04": "https://graphbz.eu/spip.php?article6222",
        "003-05": "https://graphbz.eu/spip.php?article6223",
        "004-01": "https://graphbz.eu/spip.php?article6224",
        "004-02": "https://graphbz.eu/spip.php?article6225",
        "005-01": "https://graphbz.eu/spip.php?article6226",
        "005-02": "https://graphbz.eu/spip.php?article6227",
        "005-03": "https://graphbz.eu/spip.php?article6228",
        "006-01": "https://graphbz.eu/spip.php?article6229",
        "006-02": "https://graphbz.eu/spip.php?article6231",
        "007-01": "https://graphbz.eu/spip.php?article6667",
        "007-02": "https://graphbz.eu/spip.php?article6668",
        "007-03": "https://graphbz.eu/spip.php?article6669",
        "008-01": "https://graphbz.eu/spip.php?article6233",
        "008-02": "https://graphbz.eu/spip.php?article6234",
        "008-03": "https://graphbz.eu/spip.php?article6235",
        "008-04": "https://graphbz.eu/spip.php?article6236",
        "008-05": "https://graphbz.eu/spip.php?article6237",
        "008-06": "https://graphbz.eu/spip.php?article6238",
        "008-07": "https://graphbz.eu/spip.php?article6239",
        "008-08": "https://graphbz.eu/spip.php?article6240",
        "009-01": "https://graphbz.eu/spip.php?article6241",
        "009-02": "https://graphbz.eu/spip.php?article6242",
        "009-03": "https://graphbz.eu/spip.php?article6243",
        "009-04": "https://graphbz.eu/spip.php?article6244",
        "009-05": "https://graphbz.eu/spip.php?article6245",
        "009-06": "https://graphbz.eu/spip.php?article6246",
        "010-01": "https://graphbz.eu/spip.php?article6247",
        "010-02": "https://graphbz.eu/spip.php?article6248",
        "010-03": "https://graphbz.eu/spip.php?article6249",
        "010-04": "https://graphbz.eu/spip.php?article6250",
        "010-05": "https://graphbz.eu/spip.php?article6251",
        "011-01": "https://graphbz.eu/spip.php?article6252",
        "011-02": "https://graphbz.eu/spip.php?article6253",
        "011-03": "https://graphbz.eu/spip.php?article6254",
        "011-04": "https://graphbz.eu/spip.php?article6255",
        "011-05": "https://graphbz.eu/spip.php?article6256",
        "011-06": "https://graphbz.eu/spip.php?article6257",
        "011-07": "https://graphbz.eu/spip.php?article6670",
        "012-01": "https://graphbz.eu/spip.php?article6258",
        "012-02": "https://graphbz.eu/spip.php?article6259",
        "012-03": "https://graphbz.eu/spip.php?article6260",
        "012-04": "https://graphbz.eu/spip.php?article6671",
        "013-01": "https://graphbz.eu/spip.php?article6261",
        "013-02": "https://graphbz.eu/spip.php?article6262",
        "013-03": "https://graphbz.eu/spip.php?article6263",
        "013-04": "https://graphbz.eu/spip.php?article6264",
        "013-05": "https://graphbz.eu/spip.php?article6265",
        "013-06": "https://graphbz.eu/spip.php?article6266",
        "013-07": "https://graphbz.eu/spip.php?article6267",
        "013-08": "https///graphbz.eu/spip.php?article7451",
        "014-01": "https://graphbz.eu/spip.php?article6672",
        "014-02": "https://graphbz.eu/spip.php?article6673",
        "015-01": "https://graphbz.eu/spip.php?article6674",
        "015-02": "https://graphbz.eu/spip.php?article6675",
        "016-01": "https://graphbz.eu/spip.php?article6268",
        "016-02": "https://graphbz.eu/spip.php?article6269",
        "017-01": "https://graphbz.eu/spip.php?article6270",
        "017-02": "https://graphbz.eu/spip.php?article6271",
        "018-01": "https://graphbz.eu/spip.php?article6272",
        "018-02": "https://graphbz.eu/spip.php?article6273",
        "019-01": "https://graphbz.eu/spip.php?article6274",
        "019-02": "https://graphbz.eu/spip.php?article6275",
        "019-03": "https://graphbz.eu/spip.php?article6379",
        "019-04": "https://graphbz.eu/spip.php?article6276",
        "020-01": "https://graphbz.eu/spip.php?article6277",
        "020-02": "https://graphbz.eu/spip.php?article6380",
        "020-03": "https://graphbz.eu/spip.php?article6278",
        "021-01": "https://graphbz.eu/spip.php?article6279",
        "021-02": "https://graphbz.eu/spip.php?article6280",
        "021-03": "https://graphbz.eu/spip.php?article6281",
        "022-01": "https://graphbz.eu/spip.php?article6282",
        "022-02": "https://graphbz.eu/spip.php?article6283",
        "022-03": "https://graphbz.eu/spip.php?article6284",
        "022-04": "https://graphbz.eu/spip.php?article6285",
        "022-05": "https://graphbz.eu/spip.php?article6286",
        "022-06": "https://graphbz.eu/spip.php?article6286",
        "023-01": "https://graphbz.eu/spip.php?article6288",
        "023-02": "https://graphbz.eu/spip.php?article6289",
        "023-03": "https://graphbz.eu/spip.php?article6290",
        "023-04": "https://graphbz.eu/spip.php?article6291",
        "023-05": "https://graphbz.eu/spip.php?article6292",
        "023-06": "https://graphbz.eu/spip.php?article6294",
        "023-07": "https://graphbz.eu/spip.php?article6295",
        "023-08": "https://graphbz.eu/spip.php?article6296",
        "023-09": "https://graphbz.eu/spip.php?article6297",
        "024-01": "https://graphbz.eu/spip.php?article6298",
        "024-02": "https://graphbz.eu/spip.php?article6299",
        "024-03": "https://graphbz.eu/spip.php?article6300",
        "024-04": "https://graphbz.eu/spip.php?article6301",
        "024-05": "https://graphbz.eu/spip.php?article6302",
        "024-06": "https://graphbz.eu/spip.php?article6303",
        "025-01": "https://graphbz.eu/spip.php?article6304",
        "025-02": "https://graphbz.eu/spip.php?article6305",
        "025-03": "https://graphbz.eu/spip.php?article6306",
        "025-04": "https://graphbz.eu/spip.php?article6307",
        "025-05": "https://graphbz.eu/spip.php?article6308",
        "025-06": "https://graphbz.eu/spip.php?article6309",
        "026-01": "https://graphbz.eu/spip.php?article6310",
        "026-02": "https://graphbz.eu/spip.php?article6311",
        "027-01": "https://graphbz.eu/spip.php?article6312",
        "027-02": "https://graphbz.eu/spip.php?article6313",
        "027-03": "https://graphbz.eu/spip.php?article6314",
        "028-01": "https://graphbz.eu/spip.php?article6315",
        "028-02": "https://graphbz.eu/spip.php?article6316",
        "028-03": "https://graphbz.eu/spip.php?article6676",
        "028-04": "https://graphbz.eu/spip.php?article6677",
        "028-05": "https://graphbz.eu/spip.php?article6678",
        "029-01": "https://graphbz.eu/spip.php?article6317",
        "029-02": "https://graphbz.eu/spip.php?article6318",
        "029-03": "https://graphbz.eu/spip.php?article6319",
        "029-04": "https://graphbz.eu/spip.php?article6320",
        "029-05": "https://graphbz.eu/spip.php?article6321",
        "029-06": "https://graphbz.eu/spip.php?article6322",
        "029-07": "https://graphbz.eu/spip.php?article6323",
        "029-08": "https://graphbz.eu/spip.php?article6324",
        "029-09": "https://graphbz.eu/spip.php?article6381",
        "029-10": "https://graphbz.eu/spip.php?article6325",
        "030-01": "https://graphbz.eu/spip.php?article6326",
        "030-02": "https://graphbz.eu/spip.php?article6327",
        "030-03": "https://graphbz.eu/spip.php?article6328",
        "030-04": "https://graphbz.eu/spip.php?article6329",
        "030-05": "https://graphbz.eu/spip.php?article6330",
        "030-06": "https://graphbz.eu/spip.php?article6331",
        "031-01": "https://graphbz.eu/spip.php?article6332",
        "031-02": "https://graphbz.eu/spip.php?article6333",
        "032-01": "https://graphbz.eu/spip.php?article6334",
        "032-02": "https://graphbz.eu/spip.php?article6335",
        "032-03": "https://graphbz.eu/spip.php?article6336",
        "032-04": "https://graphbz.eu/spip.php?article6337",
        "033-01": "https://graphbz.eu/spip.php?article6338",
        "033-02": "https://graphbz.eu/spip.php?article6339",
        "033-03": "https://graphbz.eu/spip.php?article6340",
        "033-04": "https://graphbz.eu/spip.php?article6341",
        "034-01": "https://graphbz.eu/spip.php?article6342",
        "034-02": "https://graphbz.eu/spip.php?article6343",
        "034-03": "https://graphbz.eu/spip.php?article6344",
        "034-04": "https://graphbz.eu/spip.php?article6345",
        "035-01": "https://graphbz.eu/spip.php?article6346",
        "035-02": "https://graphbz.eu/spip.php?article6347",
        "035-03": "https://graphbz.eu/spip.php?article6348",
        "035-04": "https://graphbz.eu/spip.php?article6349",
        "036-01": "https://graphbz.eu/spip.php?article6350",
        "036-02": "https://graphbz.eu/spip.php?article6351",
        "036-03": "https://graphbz.eu/spip.php?article6352",
        "036-04": "https://graphbz.eu/spip.php?article6353",
        "037-01": "https://graphbz.eu/spip.php?article6679",
        "037-02": "https://graphbz.eu/spip.php?article6680",
        "038-01": "https://graphbz.eu/spip.php?article6354",
        "038-02": "https://graphbz.eu/spip.php?article6355",
        "038-03": "https://graphbz.eu/spip.php?article6356",
        "038-04": "https://graphbz.eu/spip.php?article6357",
        "039-01": "https://graphbz.eu/spip.php?article6358",
        "039-02": "https://graphbz.eu/spip.php?article6359",
        "039-03": "https://graphbz.eu/spip.php?article6360",
        "039-04": "https://graphbz.eu/spip.php?article6361",
        "040-01": "https://graphbz.eu/spip.php?article6362",
        "040-02": "https://graphbz.eu/spip.php?article6363",
        "041-01": "https://graphbz.eu/spip.php?article6364",
        "041-02": "https://graphbz.eu/spip.php?article6365",
        "042-01": "https://graphbz.eu/spip.php?article6366",
        "042-02": "https://graphbz.eu/spip.php?article6367",
        "043-01": "https://graphbz.eu/spip.php?article6368",
        "043-02": "https://graphbz.eu/spip.php?article6369",
        "044-01": "https://graphbz.eu/spip.php?article6370",
        "044-02": "https://graphbz.eu/spip.php?article6371",
        "044-03": "https://graphbz.eu/spip.php?article6372",
        "044-04": "https://graphbz.eu/spip.php?article6373",
        "045-01": "https://graphbz.eu/spip.php?article6681",
        "045-02": "https://graphbz.eu/spip.php?article6682",
        "046-01": "https://graphbz.eu/spip.php?article6374",
        "046-02": "https://graphbz.eu/spip.php?article6375",
        "046-03": "https://graphbz.eu/spip.php?article6376",
        "046-04": "https://graphbz.eu/spip.php?article6377",
        "046-05": "https://graphbz.eu/spip.php?article6378"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads/'

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(500)
def page_not_found(e):
    return render_template('error500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/None', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.form:
            flash('No file part')
            return redirect(request.url)
        file = request.form['file']
        imgdata = base64.b64decode(str(file))
        try:
            tensor = transform_image(imgdata)
            prediction = get_prediction(tensor)
            pred_percent = torch.nn.functional.softmax(prediction, dim=1)
            template = fill_template(pred_percent.tolist()[0])
            return template
        except:
            return jsonify({'error': 'error during prediction'})

    return render_template('index.html')


def fill_template(probs):
    classes = ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012',
               '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024',
               '025', '026', '027', '028', '029', '030', '031', '032', '033', '034', '035', '036',
               '037', '038', '039', '040', '041', '042', '043', '044', '045', '046']
    predictions = sorted(zip(classes, map(float, probs)), key=lambda p: p[1], reverse=True)

    prediction = [str(predictions[0][0]),
                  str(predictions[1][0]),
                  str(predictions[2][0])]

    probas = [str('%.2f' % (predictions[0][1] * 100)) + "%",
              str('%.2f' % (predictions[1][1] * 100)) + "%",
              str('%.2f' % (predictions[2][1] * 100)) + "%"]

    for p in probas:
        p = "0.01%" if p == "0.00%" else p

    result1 = []
    result2 = []
    result3 = []

    vignettes_path = Path("static/images/Vignettes")

    for sub_class in sorted(Path(vignettes_path, prediction[0]).iterdir()):
        vignette_path = next(Path(sub_class).glob("*.jpg"))
        vignette_name = str(prediction[0]) + "-" + str(sub_class.name)
        result1.append((vignette_path, vignette_name, dico.get(vignette_name)))

    for sub_class in sorted(Path(vignettes_path, prediction[1]).iterdir()):
        vignette_path = next(Path(sub_class).glob("*.jpg"))
        vignette_name = str(prediction[1]) + "-" + str(sub_class.name)
        result2.append((vignette_path, vignette_name, dico.get(vignette_name)))

    for sub_class in sorted(Path(vignettes_path, prediction[2]).iterdir()):
        vignette_path = next(Path(sub_class).glob("*.jpg"))
        vignette_name = str(prediction[2]) + "-" + str(sub_class.name)
        result3.append((vignette_path, vignette_name, dico.get(vignette_name)))

    return render_template('result.html', prediction=prediction,
                           probas=probas,
                           result1=result1,
                           result2=result2,
                           result3=result3)


if __name__ == '__main__':
    app.run()
