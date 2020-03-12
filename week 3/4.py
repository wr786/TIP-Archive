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
    peopleTotalCnt = len(peopleData)
    # 5->上车时间 8->下车时间
    peopleInCarTime = [calc_in_car_time(x[5], x[8]) for x in peopleData]
    peopleNumOfTime = {}
    maxTime = -1
    peopleTargetCnt = 0.98 * peopleTotalCnt
    for t in peopleInCarTime:
        if peopleNumOfTime.get(t):
            peopleNumOfTime[t] += 1
            if maxTime == -1 or peopleNumOfTime[t] > peopleNumOfTime.get(maxTime):
                maxTime = t
        else:
            peopleNumOfTime[t] = 1
    peopleTargetCnt -= peopleNumOfTime[maxTime]
    timeLeft = maxTime
    timeRight = maxTime
    while peopleTargetCnt > 0:
        if timeLeft > 1:
            timeLeft -= 1
            peopleTargetCnt -= peopleNumOfTime.get(timeLeft)
        if timeRight > 0:
            timeRight += 1
            peopleTargetCnt -= peopleNumOfTime.get(timeRight)
    print("[INFO] 数据计算完成!")

    outputFile = open("PeopleInCarTime.txt", "w")
    for i in range(timeLeft, timeRight+1):
        outputFile.write(f"{i}分钟: {peopleNumOfTime[i]}人\n")
    outputFile.close()
    print("[INFO] 数据输出成功!")
    end_time = time.time()
    print(f"[INFO] Task Finished in {end_time - start_time}s.")
