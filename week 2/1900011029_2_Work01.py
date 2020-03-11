# -*- coding: utf-8 -*-
# author: wr786
student_id = 1900011029

# reading data
dataFile = open("./50万人名.txt", "r", encoding="utf-8")
nameData = dataFile.read()
names = nameData.splitlines()
dataFile.close()

# processing
outputFile = open(f"{student_id}_2_Work01.txt", "w", encoding="utf-8")
names.sort(key=lambda x: len(x))
cnt_2 = 0
cnt_3 = 0
cnt_4 = 0
for name in names:
    if len(name) == 2:
        cnt_2 += 1
    elif len(name) == 3:
        cnt_3 += 1
    elif len(name) == 4:
        cnt_4 += 1

outputFile.write(f"2字\t{cnt_2}\n")
outputFile.write(f"3字\t{cnt_3}\n")
outputFile.write(f"4字\t{cnt_4}\n")
outputFile.close()