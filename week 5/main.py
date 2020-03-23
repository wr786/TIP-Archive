# -*- coding:utf-8 -*-
# author: wr786
from flask import Flask, render_template, request
import os
app = Flask(__name__)

peopleData = []
# carType,icID,cardType,tradeType,UpLine,UpTime,UpStation,DownLine,DownTime,DownStation,State       
#   0       1      2        3       4       5      6         7        8         9        10
SubwayPeopleData = {} # {("HHMM", "HHMM"): cnt}

def readInData():
    print("[INFO] 程序开始运行。\n")
    f = open(os.path.join(os.path.abspath('.'), 'Subway_20180301.txt'), 'r', errors="ignore")
    cnt = 0
    for line in f:
        cnt += 1
        peopleData.append(line.split(','))
    f.close()
    peopleData.pop(0) # 去除标题行
    print("[INFO] 数据读取成功！\n")
    
def nxt_minute(t, delta=1):
    # 输入"HHMM"返回"HHMM"格式的字符串
    hur = int(t[:2])
    mnt = int(t[2:4])
    mnt += delta
    hur += mnt // 60
    hur %= 24
    mnt %= 60
    return str(hur).zfill(2) + str(mnt).zfill(2)

def get_time_interval(t, delta=5):
    # 输入"HHMMSS"返回("HHMM", "HHMM")
    hur = int(t[:2])
    mnt = int(t[2:4])
    mnt_inf = (mnt//delta)*delta
    mnt_sup = mnt_inf + delta - 1
    return (str(hur).zfill(2) + str(mnt_inf).zfill(2), str(hur).zfill(2) + str(mnt_sup).zfill(2))    

def format_time_interval(t):
    # 输入"HHMM"返回"HH:MM"
    return t[:2] + ":" + t[2:]

def calc_SubwayPeople():    
    curTime = "0000" #! 采取以00:00为0人的记录方法
    while True: # 初始化
        SubwayPeopleData.update({get_time_interval(curTime): 0})
        curTime = nxt_minute(curTime, 5)
        if curTime == "0000":
            break
    for people in peopleData:
        # 采取前缀和算法存储
        # 当前时间段如果有人进站，将他算在这个时间段的乘客之中
        # 当前时间段如果有人出站，仍然将他算在这个时间段的乘客之中，但是不把他算在下个时间段的乘客之中
        SubwayPeopleData[get_time_interval(people[5][-6:])] += 1
        SubwayPeopleData[get_time_interval(people[8][-6:])] -= 1
        # SubwayPeopleData[get_time_interval(nxt_minute(people[8][-6:-2], 5) + people[8][-2:])] -= 1

def toHex(r, g, b):
    color = "#"
    color += str(hex(r)).replace('x','0')[-2:]
    color += str(hex(g)).replace('x','0')[-2:]
    color += str(hex(b)).replace('x','0')[-2:]
    return color

def getcolor(num, lim):
    halfLim = lim / 2
    cell = 255 / halfLim
    r = 0
    g = 0
    b = 0
    if num < halfLim:
        r = int(cell * num)
        g = 255
    else:
        g = int(max(0, 255 - ((num-halfLim)*cell)))
        r = 255
    return toHex(r, g, b)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/SubwayPeople")
def SubwayPeople():
    tableSP = ""
    curCnt = 0
    for time_interval in sorted(SubwayPeopleData.keys()):
        curCnt += SubwayPeopleData[time_interval]
        if curCnt < 0:
            print(f"[WARNING] SubwayPeople at {time_interval[0]}~{time_interval[1]} reaches {curCnt}")
        tableSP += f"<tr> <td>{format_time_interval(time_interval[0])}~{format_time_interval(time_interval[1])}</td> <td>"
        tableSP += f'<div class="incar_cnt" style="width: {curCnt / 8000}%; background: {getcolor(curCnt, 800000)};">{curCnt}</div> </td></tr>'
    return render_template("SubwayPeople.html", table_innerHTML=tableSP)

if __name__ == "__main__":
    readInData()
    calc_SubwayPeople()
    app.run(debug=True) 