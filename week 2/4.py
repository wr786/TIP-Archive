# -*- coding: utf-8 -*-
# author: wr786
# student_id = 隐去私人信息

# reading data
dataFile = open("./50万人名.txt", "r", encoding="utf-8")
nameData = dataFile.read()
names = nameData.splitlines()
dataFile.close()

# processing
outputFile = open(f"{student_id}_4_Work01.txt", "w", encoding="utf-8")
dic = {}
idx = 1

for name in names:
    for ch in name[1:]:
        if ch not in dic:
            dic.update({ch: 1})
        else:
            dic[ch] += 1

for (ch, count) in (sorted(dic.items(), key=lambda x: x[1], reverse=True)):
    if idx > 200:
        break
    outputFile.write(f"{ch}\t{count}\n")
    idx += 1

outputFile.close()
