# -*- coding:utf-8 -*-
# author: wr786
from flask import Flask, render_template, request
app = Flask(__name__)

peopleData = []
# carType,icID,cardType,tradeType,UpLine,UpTime,UpStation,DownLine,DownTime,DownStation,State       
#   0       1      2        3       4       5      6         7        8         9        10

def readInData():
    dataFile = open("./Subway_20180301.txt", "r")
    data = dataFile.read()
    dataFile.close()
    for line in data.splitlines[1:]:
        peopleData.append(line.split(','))
    
def calc_SubwayPeople():
    uptimeData = sorted(peopleData, key=lambda x: x[5])
    downtimeData = sorted(peopleData, key=lambda x: x[8])
    


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/SubwayPeople")
def SubwayPeople():
    return render_template("SubwayPeople.html")

if __name__ == "__main__":
    readInData()
    calc_SubwayPeople()
    app.run(debug=True) 