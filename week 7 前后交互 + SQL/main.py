# author: wr786
from flask import Flask, session, render_template, request, redirect
import sqlite3
import hashlib
import os

app = Flask(__name__)
dbConn = sqlite3.connect('./data/userInfo.db', check_same_thread=False)

lastChess = {} # 用来存棋
blackHolder = {}
whiteHolder = {}

# 用来加密密码，避免在数据库中明文保存密码
def encrypt(pwd): 
    sha = hashlib.sha256(pwd.encode('utf-8'))
    encrypted = sha.hexdigest()
    return encrypted

@app.route('/')
def index():
    if 'userName' not in session:
        return redirect("/login")
    return render_template('index.html', userName=session['userName'])

@app.route('/receiveMsg', methods=["POST", "GET"])
def receiveMsg():
    fromSide = request.form["fromSide"]
    toSide = request.form["toSide"]
    pos_x = request.form["chess_x"]
    pos_y = request.form["chess_y"]
    sides = f'{fromSide}->{toSide}'
    antiSides = f'{toSide}->{fromSide}'
    lastChess.update({sides: (pos_x, pos_y)})
    if sides not in blackHolder.keys() and sides not in whiteHolder.keys(): # 决定先后手
        blackHolder.update({sides: fromSide})
        blackHolder.update({antiSides: fromSide})
        whiteHolder.update({sides: fromSide})
        whiteHolder.update({antiSides: fromSide})
    return "black" if blackHolder[sides] == fromSide else "white"

@app.route('/getMsg', methods=["POST", "GET"])
def getMsg():
    fromSide = request.form["fromSide"]
    toSide = request.form["toSide"]
    sides = f'{toSide}->{fromSide}'
    rtnMsg = ""
    if sides in lastChess.keys():
        pos = lastChess[sides]
        lastChess.pop(sides)
        rtnMsg = "black" if blackHolder[sides] == toSide else "white"
        rtnMsg += f',{pos[0]},{pos[1]}'
    return rtnMsg


@app.route('/login')
def login_static():
    return app.send_static_file('login.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    userName = request.form["username"].strip()
    passWord = request.form["password"]
    user = list(dbConn.execute(f"select username, password from users where username='{userName}'"))
    if len(user) == 0:
        statusMsg = "用户名不存在！"
    elif encrypt(passWord) != user[0][1]:
        statusMsg = "密码错误！"
    else:
        session['userName'] = userName
        statusMsg = "登陆成功，正在跳转到首页…"
    return render_template('loginStatus.html', loginMsg=statusMsg)

@app.route('/register')
def register_static():
    return app.send_static_file('register.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    userName = request.form["username"].strip()
    passWord = request.form["password"]
    cursor = dbConn.execute(f"select username from users where username='{userName}'")
    if (len(list(cursor))) != 0:
        statusMsg = "非常抱歉！您的用户名刚刚已经被注册！请换一个用户名注册。"
    else:
        dbConn.execute(f"insert into users(username, password) values('{userName}', '{encrypt(passWord)}')")
        dbConn.commit()
        statusMsg = "恭喜您！注册成功！"
    return render_template('registerStatus.html', registerMsg=statusMsg)

@app.route('/CheckUserID', methods=["POST", "GET"])
def checkUserID():
    userName = request.form["username"].strip()
    cursor = dbConn.execute(f"select username from users where username='{userName}'")
    if (len(list(cursor))) != 0:
        return "0"
    else:
        return "1"

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(port=80, debug=True)
    dbConn.close()

#todo 判定五子棋是否已经存在于那个位置了
#todo 判定五子棋输赢
#todo 美化棋盘
#todo 美化对局UI
#todo 美化注册、登陆UI