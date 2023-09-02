from flask import Flask, render_template, jsonify,request
from flask_mysqldb import MySQL
from camera import Camera 
from flask_cors import CORS
from twilo_messaging import send_sms





app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'securitycameraappdb'


mysql = MySQL(app)


camera = Camera()

@app.route("/")
def home():

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    fetch_data = cur.fetchall()
    cur.close()


    return render_template("home.html", data = fetch_data)



@app.route("/start")
def start():
    camera.start()

    return jsonify(message = "camera started"), 200


@app.route("/stop")
def stop():
    camera.stop()

    return jsonify(message = "camera stopped"), 200


@app.route("/motion-detected",methods=["POST"])
def motion_detected():
    data = request.get_json()
    print(data)

    if 'url' in data:
        print("URL:", data['url'])
        send_sms.send_notification(data['url'])
        

    else:
        print("url not in incoming data")
    
    return jsonify({}), 201



if __name__ == "__main__":
    app.run(debug=True)