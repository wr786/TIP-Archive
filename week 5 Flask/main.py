# -*- coding:utf-8 -*-
# author: wr786
from flask import Flask, render_template, request
import os
app = Flask(__name__)

peopleData = []
#! carType,icID,cardType,tradeType,UpLine,UpTime,UpStation,DownLine,DownTime,DownStation,State       
#!   0       1      2        3       4       5      6         7        8         9        10
stationIDs = []
stationsInLine = {} # {lineID: set(stations)}
timeIntervals_15min = []
SubwayPeopleData = {} # {("HHMM", "HHMM"): cnt}
StationIOData = {} # {stationID: {("HHMM", "HHMM"): [upCnt, downCnt]}}
LineIOData = {} # {LineID: {("HHMM", "HHMM"): [upCnt, downCnt]}}

def get_stationID(line, station):
    return str(line).zfill(2) + "->" + str(station).zfill(2)

def parse_stationID(stationID):
    pos = stationID.find('->')
    return (int(stationID[:pos]), int(stationID[pos+2:]))

def readInData():
    print("[INFO] 程序开始运行。\n")
    f = open(os.path.join(os.path.abspath('.'), 'Subway_20180301.txt'), 'r', errors="ignore")
    cnt = 0
    for line in f:
        cnt += 1
        people = line.split(',')
        if cnt > 1:
            people[4] = int(people[4])
            people[6] = int(people[6])
            people[7] = int(people[7])
            people[9] = int(people[9])
        peopleData.append(people)
    f.close()
    peopleData.pop(0) # 去除标题行
    # 计算每条line下的stations
    for people in peopleData:
        if people[4] not in stationsInLine.keys():
            stationsInLine.update({people[4]: {people[6]}})
        else:
            stationsInLine[people[4]].add(people[6])
        if people[7] not in stationsInLine.keys():
            stationsInLine.update({people[7]: {people[9]}})
        else:
            stationsInLine[people[7]].add(people[9])
    # 计算总共有哪些station
    for line in stationsInLine.keys():
        for station in stationsInLine[line]:
            if get_stationID(line, station) not in stationIDs:
                stationIDs.append(get_stationID(line, station))
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
    # 输入"HHMMSS"或"HHMM"返回("HHMM", "HHMM")
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

def calc_stationIO():
    curTime = "0000"
    while True: # 初始化timeIntevals_15min
        timeIntervals_15min.append(get_time_interval(curTime, 15))
        curTime = nxt_minute(curTime, 15)
        if curTime == "0000":
            break
    StationIOData.update({786: {("ERROR", "ERROR"): [0, 0]}}) # 占位用
    for time_interval in timeIntervals_15min: # 初始化一个计算所有站点总数的特殊key
        StationIOData[786].update({time_interval: [0, 0]})
    for stationID in stationIDs: # 初始化
        StationIOData.update({stationID: {("ERROR", "ERROR"): [0, 0]}}) # 占位用
        for time_interval in timeIntervals_15min:
            StationIOData[stationID].update({time_interval: [0, 0]})
    for people in peopleData:
        StationIOData[get_stationID(people[4], people[6])][get_time_interval(people[5][-6:], 15)][0] += 1
        StationIOData[get_stationID(people[7], people[9])][get_time_interval(people[8][-6:], 15)][1] += 1
        StationIOData[786][get_time_interval(people[5][-6:], 15)][0] += 1
        StationIOData[786][get_time_interval(people[8][-6:], 15)][1] += 1

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

def get_stationIO_cell(time_interval, cnt, divisor=50, timeTag=True, font_size=12):
    time_interval_formatted = f'{format_time_interval(time_interval[0])}~{format_time_interval(time_interval[1])}'
    upCnt = cnt[0] 
    downCnt = cnt[1]
    ret = f'<div class="tdLine"><div class="upStation" style="width: {upCnt/divisor}%;"></div><div class="upStation_inner" style="font-size:{font_size}px;">{upCnt}</div>'
    if timeTag:
        ret += f'<div class="timeTag" style="width: 10%; font-size:{font_size}px;">{time_interval_formatted}</div>'                
    ret += f'<div class="downStation" style="width: {downCnt/divisor}%;"></div><div class="downStation_inner" style="font-size:{font_size}px;">{downCnt}</div></div>'
    return ret

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

@app.route("/StationIO", methods=['GET','POST'])
def StationIO():
    selectedStations = request.form.get("checklist", False)
    formSIO = ""
    tableSIO = ""
    last = "06" # 第一行的线路编号
    for stationID in stationIDs:
        if stationID[:2] != last:
            formSIO += '<br/>'
            last = stationID[:2]
        formSIO += f'<input name="checklist" type="radio" value="{stationID}" ID="{stationID}" {"checked" if stationID == selectedStations else "unchecked"}/><label for="{stationID}">{stationID}</label>'
    #! 转置表格，不然宽度爆炸了
    if selectedStations == False:
        tableSIO += "<tr><th>所有站点</th></tr>"
        for time_interval in timeIntervals_15min:
            tableSIO += f'<tr><td>{get_stationIO_cell(time_interval, StationIOData[786][time_interval], 8000)}</td></tr>'
    else:
        tableSIO += f"<tr><th>{selectedStations}</th></tr>"
        for time_interval in timeIntervals_15min:
            tableSIO += f"<tr><td>{get_stationIO_cell(time_interval, StationIOData[selectedStations][time_interval])}</td></tr>"
    return render_template("StationIO.html", table_innerHTML=tableSIO, form_innerHTML=formSIO)

@app.route("/LineIO", methods=['GET', 'POST'])
def LineIO():
    # 统计每条线路IO总数
    for line in stationsInLine.keys(): # 初始化
        LineIOData.update({line: {('ERROR', 'ERROR'): [0, 0]}})
        for time_interval in timeIntervals_15min:
            LineIOData[line].update({time_interval: [0, 0]})
    for station in StationIOData.keys():
        # print(f"[DEBUG] station = {station}")
        if station == 786: # 跳过占位的
            continue
        line = parse_stationID(str(station))[0]
        for time_interval in timeIntervals_15min:
            LineIOData[line][time_interval][0] += StationIOData[station][time_interval][0]
            LineIOData[line][time_interval][1] += StationIOData[station][time_interval][1]
    selectedLines = request.form.get("checklist", False) # 后面才发现是只要一条线路就行，但懒得改了，就当作这是只有一个元素的list吧
    formLIO = ""
    tableLIO = ""
    hint_data = ""
    for line in stationsInLine.keys():
        formLIO += f'<input name="checklist" type="radio" value="{line}" ID="{line}" {"checked" if int(line) == int(selectedLines) else "unchecked"} /><label for="{line}">{str(line).zfill(2)}</label>'
    #! 同样地，转置表格
    if selectedLines != False: 
        tableLIO += '<tr><th>时间段</th>'
        for station in stationsInLine[int(selectedLines[0])]:
            tableLIO += f'<th>{station}</th>'
        tableLIO += '</tr>'
        for time_interval in timeIntervals_15min:
            tableLIO += f'<tr><td>{format_time_interval(time_interval[0])}~{format_time_interval(time_interval[1])}</td>'
            for station in stationsInLine[int(selectedLines[0])]:
                station_id = get_stationID(selectedLines[0], station)
                tableLIO += f'<td>{get_stationIO_cell(time_interval, StationIOData[station_id][time_interval], 80, False, 2)}</td>'
            tableLIO += '</tr>'
        hint_data = "线路" + selectedLines + "的各个站点"
    else: # 显示线路表
        tableLIO += '<tr><th>时间段</th>'
        for line in LineIOData.keys():
            tableLIO += f'<th>{str(line).zfill(2)}</th>'
        tableLIO += '</tr>'
        for time_interval in timeIntervals_15min:
            tableLIO += f'<tr><td>{format_time_interval(time_interval[0])}~{format_time_interval(time_interval[1])}</td>'
            for line in LineIOData.keys():
                tableLIO += f'<td>{get_stationIO_cell(time_interval, LineIOData[line][time_interval], 500, False, 2)}</td>'
            tableLIO += '</tr>'
        hint_data = "各个线路"
    return render_template("LineIO.html", table_innerHTML=tableLIO, form_innerHTML=formLIO, hint=hint_data)

if __name__ == "__main__":
    readInData()
    calc_SubwayPeople()
    calc_stationIO()
    app.run(debug=True) 

#todo 加上select
#todo 加上图标
#todo 给标题加上avatar
#todo 美化UI