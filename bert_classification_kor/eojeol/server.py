# flask_app/server.py​
import datetime
import re

from flask_ngrok import run_with_ngrok 
from flask import Flask, request, jsonify, render_template, session, url_for, redirect
from flask_dropzone import Dropzone
import time
from urllib.parse import unquote
import os
import uuid
import secrets

from run_intent_classify import sentiment_predict, csv_predict
from settings import *
import requests
import pdb

from input_module import read_file

app = Flask(__name__)

# colab에서의 서빙을 위해 flask_ngrok 모듈의 run_with_ngrok 함수를 사용합니다.
run_with_ngrok(app)

UPLOAD_FOLDER = os.path.join(app.root_path,'upload_files')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'text'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(
    SECRET_KEY=secrets.token_urlsafe(32),
    SESSION_COOKIE_NAME='InteractiveTransformer-WebSession'
)

dropzone = Dropzone(app)

def delay_func(func):
    def inner(*args, **kwargs):
        returned_value = func(*args, **kwargs)
        time.sleep(0)
        return returned_value
    return inner

# 실행 시작
@app.route("/")
def index():
    # 처음 보여지는 화면입니다. 
    return render_template("index.html")

@app.route('/_evaluate_helper')
def evaluate_helper():
    eval_text = request.args.get("evaluate_data", "", type=str).strip()
    eval_text = re.sub("%20", "", eval_text)
    prediction = sentiment_predict(eval_text)
    
    if prediction and eval_text:
        return jsonify(result=render_template('live_eval.html', predict=[prediction[0]], eval_text=[eval_text], intent=[prediction[1]]))
    return jsonify(result="")

@app.route('/_evaluate_helper_file', methods=['POST'])
def evaluate_helper_file():
    if 'file' not in request.files:
        print('No file part')
    else:
        file = request.files.get('file')
        print(file)
    input_df = read_file(file)
    prediction = csv_predict(input_df)
      
    return jsonify(result=render_template("result_file.html", predict=[prediction]))

if __name__ == '__main__':
    #app.run(host="0.0.0.0", debug=True, port=PORT)
    app.run()
