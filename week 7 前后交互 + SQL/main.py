# author: wr786
from flask import Flask, session, render_template, request
import sqlite3
import hashlib

app = Flask(__name__)

# 用来加密密码，避免在数据库中明文保存密码
def encrypt(pwd): 
    sha = hashlib.sha256(pwd)
    encrypted = sha.hexdigest()
    return encrypted

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)