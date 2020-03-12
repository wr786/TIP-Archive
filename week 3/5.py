# -*- coding: utf-8 -*-
# author: wr786
import time


def calc_in_car_time(up_time, down_time):
    up_time = up_time[-6:]
    down_time = down_time[-6:]
    d_hour = int(down_time[:2]) - int(up_time[:2])
    d_min = int(down_time[2:4]) - int(up_time[2:4])
    d_sec = int(down_time[-2:]) - int(up_time[-2:])
    if d_sec < 0:
        d_sec += 60
        d_min -= 1
    if d_min < 0:
        d_min += 60
        d_hour -= 1
    d_total_min = 60 * d_hour + d_min + ((d_sec + 60) // 60)
    return d_total_min


if __name__ == '__main__':
    start_time = time.time()
    sourceFile = open("./Subway_20180301.txt", "r")
    data = sourceFile.read()
    sourceFile.close()
    print("[INFO] 数据读取成功!")

    dataLines = data.splitlines()
    peopleData = [x.split(",") for x in dataLines[1:]]  # 去掉标题行
    # 1->ID 5->上车时间 8->下车时间
    peopleID = set()
    timeOfID = {}
    for people in peopleData:
        if people[1] not in peopleID:
            peopleID.add(people[1])
            timeOfID.update({people[1]: (people[5], people[8])})
        else:
            timeOfID[people[1]] = (min(timeOfID[people[1]][0], people[5]), max(timeOfID[people[1]][1], people[8]))
    individualCnt = len(peopleID)
    print("[INFO] ID数据统计成功!")

    peopleOutHomeTime = {x: calc_in_car_time(timeOfID[x][0], timeOfID[x][1]) for x in timeOfID.keys()}
    peopleOHTAbove180 = {k: v for (k, v) in peopleOutHomeTime.items() if v > 180}
    totalInConsider = len(peopleOHTAbove180)  # 统计范围中的人数
    targetInConsider = totalInConsider * 0.98
    curAddTime = 0

    outputDict = {}

    while targetInConsider > 0:
        curTimePeoCnt = 0
        for v in peopleOHTAbove180.values():
            if 180 + curAddTime <= v < 185 + curAddTime:
                curTimePeoCnt += 1
        outputDict.update({180+curAddTime: curTimePeoCnt})
        curAddTime += 5
        targetInConsider -= curTimePeoCnt

    outputList = sorted(zip(outputDict.values(), outputDict.keys()), key=lambda x: -x[0]) # 从高到低排序
    print("[INFO] 数据处理完成!")

    outputFile = open("PeopleOutHomeTime.txt", "w")
    for item in outputList:
        outputFile.write(f"{item[1]}~{item[1]+4}分钟: {item[0]}人\n")
    outputFile.close()
    print("[INFO] 数据输出成功!")

    end_time = time.time()
    print(f"[INFO] Task Finished in {end_time - start_time}s.\n")
