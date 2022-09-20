from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import hashlib

app = Flask(__name__)

client = MongoClient('localhost', 27017)  
db = client.dbweek0

@app.route('/')
def home():
    return render_template('index.html')

# memo 불러오기
@app.route('/memo', methods=['GET'])
def listing():
    # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
    # 2. memo_list라는 키 값으로 모든 메모 리스트로 내려주기
    memo_list = list(db.memo.find({},{'_id':False}))
    return jsonify({'result':'success', 'memo_list': memo_list})

## API 역할을 하는 부분
@app.route('/signup', methods=['POST'])
def signUp():
    # 1. 클라이언트로부터 데이터를 받기
    # 2. 암호화
    # 3. mongoDB에 데이터 넣기
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    email_receive = request.form['email_give']
    
    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    db.users.insert_one({'id':id_receive, 'pw':pw_hash}, 'email':email_receive)
    return jsonify({'result': 'success', 'msg':'회원가입 완료!'})

# 기본포트 5000
if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)

