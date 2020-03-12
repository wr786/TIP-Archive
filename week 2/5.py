# -*- coding: utf-8 -*-
# author: wr786
# student_id = 隐去私人信息

# reading data
dataFile = open("./50万人名.txt", "r", encoding="utf-8")
nameData = dataFile.read()
names = nameData.splitlines()
dataFile.close()

# processing
outputFile = open(f"{student_id}_5_Work01.txt", "w", encoding="utf-8")
dic = {}

for name in names:
    for (index, ch) in enumerate(name[1:]):
        if name[1:].find(ch*2, index) != -1:
            if ch*2 not in dic:
                dic.update({ch*2: 1})
            else:
                dic[ch*2] += 1

for (ch, count) in (sorted(dic.items(), key=lambda x: x[1], reverse=True)):
    outputFile.write(f"{ch}\t{count}\n")

outputFile.close()
