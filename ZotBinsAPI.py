from flask import Flask, jsonify, request, flash, redirect, url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename
import os
import subprocess
import pymysql
import pandas
import queries
import config
import barcodeQueries

UPLOAD_FOLDER = '/home/zotbins/trashPics' # where we store the uploaded folder
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.secret_key = 'CkDBNwtWrvgKBpm49Ey5uQ'
app.config["DEBUG"] = True

@app.route('/')
def index():
    return "z o o t b i n s"

@app.route('/test')
def testinglala():
    return "hello ting ting"

def allowed_file(filename):
    """
    Checks whether or not the extension name is allowed.
    """
    return '.' in filename and filename.rsplit('.', 1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/observation/add/image', methods=['GET','POST'])
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
        img_path = UPLOAD_FOLDER + '/' + file.filename
        if os.path.isfile(img_path):
            return"Image already exists", 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/observation/get/image-list', methods=['GET'])
def image_names():
    onlyfiles = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return jsonify({"imageNames":onlyfiles})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    This function is for viewing the uploaded files we have
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/observation/add', methods=['POST'])
def add_observation():
    con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)

    if request.method == 'POST':
        if not request.json:
            abort(400)
        try:
            post_data = request.json
            with con.cursor() as cur:
                for obs in post_data:
                    timestamp = obs["timestamp"]
                    sensor_id = obs["sensor_id"]
                    obs_type = obs["type"]
                    if obs_type == 5:
                        cur.execute(queries.add_f_observation, (timestamp, sensor_id))
                        continue
                    measurement = None
                    if obs_type == 2:
                        measurement = obs["payload"]["weight"]
                    elif obs_type == 3:
                        measurement = obs["payload"]["distance"]
                    cur.execute(queries.add_wd_observation, (timestamp, sensor_id, obs_type, measurement))
                con.commit()
                return "added all observations"
        except Exception as e:
            print(e)
            return str(e)

@app.route('/observation/get', methods=['GET'])
def get_observation():
    try:
        con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)
        ret = []
        if request.method == 'GET':
            sensor_id = request.args.get("sensor_id")
            start_timestamp = request.args.get("start_timestamp")
            end_timestamp = request.args.get("end_timestamp")
            obs_type = None
            if sensor_id is not None or start_timestamp is not None or end_timestamp is not None:
                with con.cursor() as cur:
                    if sensor_id[-1] == 'B':
                        obs_type = 5
                        cur.execute(queries.get_f_observation, (sensor_id, start_timestamp, end_timestamp))
                        res = cur.fetchall()
                    else:
                        if sensor_id[-1] == 'D':
                            obs_type = 3
                        else:
                            obs_type = 2
                        cur.execute(queries.get_wd_observation, (sensor_id, start_timestamp, end_timestamp))
                        res = cur.fetchall()
                for obs in res:
                    obs_dict = {"sensor_id" : obs["sensor_id"], "id" : obs["id"], "timestamp" : obs["timestamp"].strftime("%m-%d-%Y %H:%M:%S")}
                    if obs_type == 3:
                        obs_dict["payload"] = {"distance":obs["measurement"]}
                    elif obs_type == 2:
                        obs_dict["payload"] = {"weight":obs["measurement"]}
                    else:
                        obs_dict["payload"] = {}
                    ret.append(obs_dict)
        return jsonify(ret)
    except Exception as e:
        print(e)
        return str(e)


@app.route('/observation/count', methods=['GET'])
def count_observation():
    try:
        con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)
        if request.method == 'GET':
            sensor_id = request.args.get("sensor_id")
            start_timestamp = request.args.get("start_timestamp")
            end_timestamp = request.args.get("end_timestamp")
            if sensor_id is not None and start_timestamp is not None and end_timestamp is not None:
                with con.cursor() as cur:
                    if sensor_id[-1] == 'B':
                        cur.execute(queries.get_f_count, (sensor_id, start_timestamp, end_timestamp))
                        res = cur.fetchone()["COUNT(*)"]
                    else:
                        cur.execute(queries.get_wd_count, (sensor_id, start_timestamp, end_timestamp))
                        res = cur.fetchone()["COUNT(*)"]
                    ret = {"sensor_id":sensor_id, "count":res, "start_timestamp":start_timestamp, "end_timestamp":end_timestamp}
                    return ret
            else:
                return "incorrect or missing query params"
    except Exception as e:
        print(e)
        return str(e)

@app.route('/barcode/add', methods=['POST'])
def addBarcode():
    con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)

    if request.method == 'POST':
        if not request.json:
            abort(400)
        try:
            post_data = request.json
            with con.cursor() as cur:
                for obs in post_data:
                    name = obs["name"]
                    myType = obs["type"]
                    barcode = obs["barcode"]
                    wasteBin = obs["wasteBin"]
                    instructions = obs["instructions"]


                    cur.execute(barcodeQueries.insert_query, (name, myType, barcode, wasteBin, instructions))

                con.commit()
                return "added all observations"
        except Exception as e:
            print(e)
            return str(e)

@app.route('/barcode/get', methods=['GET'])
def get_barcode():
    try:
        con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)
        res = []
        if request.method == 'GET':
            barcode = request.args.get("barcode")
            with con.cursor() as cur:
                if barcode is not None:
                    cur.execute(barcodeQueries.get_query, (barcode,))
                    res = cur.fetchone()
                else:
                    name = None
                    myType = None
                    barcode = barcode
                    wasteBin = None
                    instructions = None
                    cur.execute(barcodeQueries.insert_query, (name, myType, barcode, wasteBin, instructions))
                    con.commit()
                    return "added empty barcode"
        return jsonify(res)
    except Exception as e:
        print(e)
        return str(e)

# https://zotbins.pythonanywhere.com/observation/stats?sensor_id=ZBin3B&start_timestamp=2020-02-04&end_timestamp=2020-02-05
# https://zotbins.pythonanywhere.com/observation/stats?sensor_id=ZBin1D&start_timestamp=2020-02-18&end_timestamp=2020-02-20
@app.route('/observation/stats', methods=['GET'])
def get_obervation_stats():
    try:
        con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)
        resp = "could not generate csv file"
        if request.method == 'GET':
            sensor_id = request.args.get("sensor_id")
            start_timestamp = request.args.get("start_timestamp")
            end_timestamp = request.args.get("end_timestamp")
            obs_type = None

            if sensor_id is not None or start_timestamp is not None or end_timestamp is not None:
                with con.cursor() as cur:
                    if sensor_id[-1] == 'B':
                        obs_type = 5
                        cur.execute(queries.get_f_observation, (sensor_id, start_timestamp, end_timestamp))
                        res = cur.fetchall()
                    else:
                        if sensor_id[-1] == 'D':
                            obs_type = 3
                        else:
                            obs_type = 2
                        cur.execute(queries.get_wd_observation, (sensor_id, start_timestamp, end_timestamp))
                        res = cur.fetchall()

                obs_dict = {"id":[], "timestamp":[], "data":[]}
                for obs in res:
                    # obs_dict["sensor_id"].append(obs["sensor_id"])
                    obs_dict["id"].append(obs["id"])
                    obs_dict["timestamp"].append(obs["timestamp"])
                    if obs_type == 3:
                        obs_dict["data"].append(obs["measurement"])
                    elif obs_type == 2:
                        obs_dict["data"].append(obs["measurement"])

                if obs_type == 5:
                    obs_dict.pop("data") # delete data column for breakbeam response
                file_name = sensor_id + "_" + start_timestamp + "_" + end_timestamp + ".csv"
                df = pandas.DataFrame(obs_dict)
                resp = make_response(df.to_csv(index=False))
                resp.headers["Content-Disposition"] = "attachment; filename=" + file_name
                resp.headers["Content-Type"] = "text/csv"
        return resp
    except Exception as e:
        print(e)
        return str(e)



if __name__ == '__main__':
    app.run()
