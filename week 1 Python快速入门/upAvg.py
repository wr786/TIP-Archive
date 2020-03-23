#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: 1900011029 王锐

if __name__ == '__main__':
	studentsNum = int(input("[INPUT] 请输入班级学生总数:\n>>> "))
	print(f'[INFO] 请在接下来的{studentsNum}行中，每行依次输入"学生姓名 对应成绩"')
	# E.g. 小明 100
	Students = []
	totalScore = 0

	for _i in range(studentsNum):
		(curName, curScore) = input(">>> ").split()
		curScore = int(curScore)
		Students.append((curName, curScore))
		totalScore = totalScore + curScore

	avgScore = totalScore / studentsNum

	print(f'[LIST]\t姓名\t成绩')
	for student in Students:
		if student[1] >= avgScore:
			print(f'[LIST]\t{student[0]}\t{student[1]}')