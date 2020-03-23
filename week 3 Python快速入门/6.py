# -*- coding: utf-8 -*-
# author: wr786
import time


if __name__ == '__main__':
    start_time = time.time()
    sourceFile = open("./Subway_20180301.txt", "r")
    data = sourceFile.read()
    sourceFile.close()
    print("[INFO] 数据读取成功!")

    dataLines = data.splitlines()
    peopleData = [x.split(",") for x in dataLines[1:]]  # 去掉标题行
    # 4->UpLine 7->DownLine
    # 6->UpStation 9->DownStation
    peoCntOfStationCombo = {}
    for peo in peopleData:
        if not peoCntOfStationCombo.get((f"{peo[4]}:{peo[6]}", f"{peo[7]}:{peo[9]}")):
            peoCntOfStationCombo.update({(f"{peo[4]}:{peo[6]}", f"{peo[7]}:{peo[9]}"): 1})
        else:
            peoCntOfStationCombo[(f"{peo[4]}:{peo[6]}", f"{peo[7]}:{peo[9]}")] += 1
    outputList = sorted(zip(peoCntOfStationCombo.values(), peoCntOfStationCombo.keys()), key=lambda x: -x[0])
    print("[INFO] 数据处理成功!")

    outputFile = open("PeopleBtwStation.txt", "w")
    for idx in range(min(200, len(outputList))):
        outputFile.write(f"{outputList[idx][1][0]}->{outputList[idx][1][1]}: {outputList[idx][0]}人\n")
    outputFile.close()
    print("[INFO] 数据输出成功!")

    end_time = time.time()
    print(f"[INFO] Task Finished in {end_time - start_time}s.\n")
