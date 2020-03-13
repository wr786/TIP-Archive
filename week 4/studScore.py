# -*- coding:utf-8 -*-
# author: wr786
from flask import Flask, render_template, request

app = Flask(__name__)
sourceFile = open("./poetScore.txt", "r", encoding="utf-8")
poetScores = [x.split(",") for x in sourceFile.read().splitlines()[1:]]
sourceFile.close()
# 0=>姓名 1=>平时成绩 2=>期中成绩 3=>期末成绩 4=>总成绩
TYPE = ["姓名", "平时成绩", "期中成绩", "期末成绩", "总成绩"]
for poet in poetScores: # 计算总成绩
    for i in range(1, 4):
        poet[i] = int(poet[i])
    poet.append(round(poet[1] * 0.3 + poet[2] * 0.3 + poet[3] * 0.4))

def sort_list(sort_type, sort_order):
    poetScores.sort(reverse=True if sort_order == -1 else False, key=lambda x:x[sort_type])

def judge_color(score) :
    if score >= 85:
        return "green"
    elif score >= 60:
        return "yellow"
    else:
        return "red"

@app.route("/")
def index():
    sort_list(4, -1) # 默认总成绩降序
    scoretable = []
    for poet in poetScores:
        curRow = "<tr>"
        for item in poet:
            curRow += f"<td>{item}</td>"
        # 加入可视化
        curRow += f'<td class="visual"><div class="{judge_color(poet[4])} stateDiv" style="width: {poet[4]}%;">{poet[4]}</div></td>'
        curRow += "</tr>"
        scoretable.append(curRow)
    return render_template("score.html", student_score_table="\n".join(scoretable), sort_type="总成绩 降序", total_score_checked="checked", down_order_checked="checked")


@app.route("/", methods=["POST", "GET"])
def show_scores():
    sort_method = int(request.form["sort_method"])
    sort_order = int(request.form["sort_order"])
    sort_list(sort_method, sort_order)
    scoretable = []
    for poet in poetScores:
        curRow = "<tr>"
        for item in poet:
            curRow += f"<td>{item}</td>"
        # 加入可视化
        curRow += f'<td class="visual"><div class="{judge_color(poet[4])} stateDiv" style="width: {poet[4]}%;">{poet[4]}</div></td>'
        curRow += "</tr>"
        scoretable.append(curRow)
    sortType = TYPE[sort_method] + " " + ("降序" if sort_order == -1 else "升序")
    return render_template("score.html", student_score_table="\n".join(scoretable),sort_type=sortType,\
                            name_checked="checked" if sort_method == 0 else "unchecked", usual_score_checked="checked" if sort_method == 1 else "unchecked",\
                            midterm_score_checked="checked" if sort_method == 2 else "unchecked", final_score_checked="checked" if sort_method == 3 else "unchecked",\
                            total_score_checked="checked" if sort_method == 4 else "unchecked", up_order_checked="checked" if sort_order == 1 else "unchecked",\
                            down_order_checked="checked" if sort_order == -1 else "unchecked")


if __name__ == '__main__':
    app.run(debug=True)
