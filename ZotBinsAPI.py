from flask import Flask, jsonify, request
import pymysql
import queries
import config

app = Flask(__name__)

app.config["DEBUG"] = True

@app.route('/')
def index():
    return "z o o t b i n s"

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
                print(obs)
                print(obs["timestamp"].strftime("%m-%d-%Y %H:%M:%S"))
                obs_dict = {"sensor_id" : obs["sensor_id"], "id" : obs["id"], "timestamp" : obs["timestamp"].strftime("%m-%d-%Y %H:%M:%S")}
                if obs_type == 3:
                    obs_dict["payload"] = {"distance":obs["measurement"]}
                elif obs_type == 2:
                    obs_dict["payload"] = {"weight":obs["measurement"]}
                else:
                    obs_dict["payload"] = {}
                ret.append(obs_dict)
    return jsonify(ret)


@app.route('/observation/count', methods=['GET'])
def count_observation():
    con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)
    is_bad_input = 0
    if request.method == 'GET':
        sensor_id = request.args.get("sensor_id")
        start_timestamp = request.args.get("start_timestamp")
        end_timestamp = request.args.get("end_timestamp")
        # if sensor_id is None or start_timestamp is None or end_timestamp is None:
        #     is_bad_input = 1
        if sensor_id is not None or start_timestamp is not None or end_timestamp is not None:
            with con.cursor() as cur:
                if sensor_id[-1] == 'B':
                    obs_type = 5
                    cur.execute(queries.get_f_count, (sensor_id, start_timestamp, end_timestamp))
                    res = cur.fetchone()["COUNT(*)"]
                else:
                    if sensor_id[-1] == 'D':
                        obs_type = 3
                    else:
                        obs_type = 2
                    cur.execute(queries.get_wd_count, (sensor_id, start_timestamp, end_timestamp))
                    res = cur.fetchone()["COUNT(*)"]
                ret = {"sensor_id":sensor_id, "count":res, "start_timestamp":start_timestamp, "end_timestamp":end_timestamp}
                return ret
        else:
            return "incorrect or missing query params"


if __name__ == '__main__':
    app.run()
