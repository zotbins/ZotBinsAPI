from flask import Flask, jsonify, request
import pymysql
import queries
import config

app = Flask(__name__)

app.config["DEBUG"] = True

con = pymysql.connect(config.host, config.user, config.pw, config.db, cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
    return "hello world"

@app.route('/createtable/frequency')
def create_f_table():
    try:
        with con.cursor() as cur:
            cur.execute(queries.create_f_table)
        con.commit()
        return "done"
    except Exception as e:
        print("ERROR:", e)
        return "error"

@app.route('/createtable/weightdistance')
def create_wd_table():
    try:
        with con.cursor() as cur:
            cur.execute(queries.create_wd_table)
        con.commit()
        return "done"
    except Exception as e:
        print("ERROR:", e)
        return "error"

@app.route('/observation/add', methods=['POST'])
def add_observation():
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
            return "error"

@app.route('/observation/get', methods=['GET'])
def get_observation():
    ret = []
    if request.method == 'GET':
        query_data = request.json
        print(query_data)
        sensor_id = query_data["sensor_id"]
        start_timestamp = query_data["start_timestamp"]
        end_timestamp = query_data["end_timestamp"]
        obs_type = None
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
            obs_dict = {"sensor_id":obs["sensor_id"], "id":obs["id"], "timestamp":obs["timestamp"]}
            if obs_type == 3:
                obs_dict["payload"] = {"distance":obs["measurement"]}
            elif obs_type == 2:
                obs_dict["payload"] = {"weight":obs["measurement"]}
            else:
                obs_dict["payload"] = {}
            ret.append(obs_dict)
    return jsonify(ret)


if __name__ == '__main__':
    app.run()
