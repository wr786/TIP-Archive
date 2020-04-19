

stuID = "0"
file = open(f"{stuID}_StatData.txt", "r", encoding="utf-8")

lines = file.read().splitlines()
file.close()

output = open(f"{stuID}_ComputingData.txt", "w", encoding="utf-8")

# 第四题 ######################################################################################################

output.write("==================T4==================\n")

dic = {}
bases = []  # 用于存放最基层统计单位，防止重复运算

for line in lines:
    try:    # 判断后三位是否是数字，后三位是数字才是我们想要的
        num = int(line[-3:])
        if num not in dic.keys():
            dic.update({num: 1})
        else:
            dic[num] += 1
        bases.append(line.strip())
    except ValueError:
        pass

# for key in sorted(dic.keys()):
#     print(f"{key}:{dic[key]}")

for key in sorted(dic.keys()):
    output.write(f"{key}: {dic[key]}\n")


# 第五题 ######################################################################################################
# 内蒙古和河南分别是15和41

output.write("==================T5==================\n")

wordCountNMG = {}

for base in bases:
    if int(base[:2]) == 15 and base.find('村委会') != -1:
        base = base[12:-3]  # 去除数字
        base = base.replace('村委会', '')  # 去除村委会
        for letter in base:
            if letter not in wordCountNMG.keys():
                wordCountNMG.update({letter: 1})
            else:
                wordCountNMG[letter] += 1


topWordsNMG = sorted(zip(wordCountNMG.keys(), wordCountNMG.values()), key=lambda x:x[1], reverse=True)

wordCountHN = {}

for base in bases:
    if int(base[:2]) == 41 and base.find('村委会') != -1:
        base = base[12:-3]  # 去除数字
        base = base.replace('村委会', '')  # 去除村委会
        for letter in base:
            if letter not in wordCountHN.keys():
                wordCountHN.update({letter: 1})
            else:
                wordCountHN[letter] += 1

topWordsHN = sorted(zip(wordCountHN.keys(), wordCountHN.values()), key=lambda x:x[1], reverse=True)

# print('常用字\t内蒙古\t\t河南')
# for i in range(100):
#     print(f'{i+1}.\t{topWordsNMG[i][0]}:\t{topWordsNMG[i][1]}\t{topWordsHN[i][0]}\t{topWordsHN[i][1]}')
output.write('常用字\t内蒙古\t\t河南\n')
for i in range(100):
    output.write(f'{i+1}.\t{topWordsNMG[i][0]}:\t{topWordsNMG[i][1]}\t{topWordsHN[i][0]}\t{topWordsHN[i][1]}\n')

# 第六题 ######################################################################################################

names = set('李王张刘陈杨赵黄周吴徐孙胡朱高林何郭马罗梁宋郑谢韩唐冯于董萧程曹袁邓许傅沈曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段漕钱汤尹黎易常武乔贺赖龚文')
namesCnt = {}

for line in lines:
    if line.find('\t\t\t\t') != -1 or line.find('\t\t\t') != -1:    # 仅统计最低两个层次
        curLine = line.strip()
        try:    # 去掉数字
            num = int(line[-3:])    # 判断是否是最基层
            curLine = curLine[12:-3]
        except ValueError:
            curLine = curLine[12:]
        if curLine[0] in names:
            if curLine[0] in namesCnt.keys():
                namesCnt[curLine[0]] += 1
            else:
                namesCnt.update({curLine[0]: 1})

output.write("==================T6==================\n")

for name in names:
    output.write(f"{name}: {namesCnt[name]}\n")

output.close()