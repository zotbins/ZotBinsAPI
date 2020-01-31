from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'gschoe.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'gschoe'
app.config['MYSQL_PASSWORD'] = 'trash123'
app.config['MYSQL_DB'] = 'gschoe$zotbins'

mysql = MySQL(app)


@app.route('/')
def index():
    return "hello world"

@app.route('/createtable')
def create_table():
    cur = mysql.connection.cursor()
    cur.execute("CREATE TABLE Sample(id INT NOT NULL AUTO_INCREMENT, content VARCHAR(100) NOT NULL, PRIMARY KEY (id));")
    mysql.connection.commit()
    cur.close()
    return "done"

@app.route('/observation', methods=['POST'])
def add_observation():
    if request.method == 'POST':
        if not request.json:
            abort(400)
        post_data = request.json
        for observation in post_data:
            print("TIMESTAMP: ", observation["timestamp"])
    return jsonify(post_data)

# for each observation get the sensor id and type
# if type == 11
# push to FREQUENCY table everything
# if type == 2 or 3
# push to DISTANCE or WEIGHT table

if __name__ == '__main__':
    app.run()
