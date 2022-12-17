from flask import Flask, redirect, render_template, request, send_file, jsonify, session
from flask_cors import CORS, cross_origin
# from flask_session import Session
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from datetime import datetime, timedelta

from main import preprocess_data, result_data
import sqlite3
import pandas as pd
import os

app = Flask(__name__)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] ="filesystem"
# Session(app)
cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

ALLOWED_EXTENSIONS = {'csv'}

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=2)
jwt = JWTManager(app)

def get_db_connection():
    conn = sqlite3.connect('skripsi.db')
    conn.row_factory = sqlite3.Row
    return conn

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#LOGIN API
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if type(data) is dict:
                data["access_token"] = access_token 
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response

@app.route('/token', methods=["POST"])
def create_token():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "Admin" or password != "admin123":
        return {"msg": "Username dan/atau password anda salah!"}, 401

    access_token = create_access_token(identity=username)
    response = {"access_token":access_token, "msg": "Success login"}
    return response

@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@app.route("/get_cluster", methods=["POST"])
# @cross_origin(origin='*',headers=['Content-Type'])
@jwt_required()
def get_cluster():
    conn = get_db_connection()
    cursor = conn.cursor()

    file = request.files['file']
    if file and allowed_file(file.filename):
        # file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        # # print(file.read())
        # file.save(file_path)
        preprocess = preprocess_data(request.files.get('file'))
        hasil_cluster = result_data(preprocess)
        # list_cluster = []
        tuple_cluster = []
        for index, hasil in hasil_cluster.iterrows():
            # temp = {
            #     'tgl': hasil['tgl'],
            #     'ot': hasil['ot'],
            #     'lat': hasil['lat'],
            #     'lon': hasil['lon'],
            #     'depth': hasil['depth'],
            #     'mag': hasil['mag'],
            #     'remark': hasil['remark'],
            # }
            # list_cluster.append(temp)
            tuple_cluster.append((hasil['tgl'], hasil['ot'], hasil['lat'], hasil['lon'], hasil['depth'], hasil['mag'], hasil['remark'], hasil['klaster']))
        
        cursor.execute("DELETE FROM list_cluster")
        cursor.executemany("INSERT INTO list_cluster (tgl, ot, lat, lon, depth, mag, remark, cluster) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            tuple_cluster
                        )

        conn.commit()
        conn.close()
        # print(preprocess)
        return "success"

@app.route('/get_list_cluster', methods=['POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'])
def get_list_cluster():
    conn = get_db_connection()
    cursor = conn.cursor()

    result = cursor.execute("SELECT * FROM list_cluster").fetchall()

    list_cluster = []
    for res in result:
        temp = {
            'cluster': res[8],
            'tgl': res[1],
            'ot': res[2],
            'lat': res[3],
            'lon': res[4],
            'depth': res[5],
            'mag': res[6],
            'remark': res[7],
        }
        list_cluster.append(temp)
    return jsonify(result = list_cluster)

# @app.route('/')
# def index():
#     if not session.get("name"):
#         return redirect('/login')
#     return render_template('index.html')
    
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         if request.form['username']=='Admin' and request.form['password']=='admin123':
#             session['name'] = request.form.get("username")
#             return redirect("/")
#     return render_template('index.html')

# @app.route('/logout')
# def logout():
#     session['name'] = None
#     return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)