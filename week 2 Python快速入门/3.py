# -*- coding: utf-8 -*-
# author: wr786
# student_id = 隐去私人信息

# reading data
dataFile = open("./50万人名.txt", "r", encoding="utf-8")
nameData = dataFile.read()
names = nameData.splitlines()
dataFile.close()

# processing
outputFile = open(f"{student_id}_3_Work01.txt", "w", encoding="utf-8")
dic = {}

for name in names:
    if name[0] not in dic:
        dic.update({name[0]: 1})
    else:
        dic[name[0]] += 1

for (name, count) in sorted(dic.items(), key=lambda x:x[1], reverse=True):
    outputFile.write(f"{name}\t{count}\n")

outputFile.close()
