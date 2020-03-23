# author: 1900011029 王锐

class MulTable():

	def __init__(self):
		self._rowNum = 9

	def _printRow(self, row):
		for col in range(1, 10):
			if col < row:
				print(" "*6, end=" ")
			else:
				print(f"{row}*{col}=", end="")
				if row * col < 10:
					print('', end=" ")
				print(f"{row*col}", end=" ")
		print("\n")


	def show(self):
		for rowIdx in range(1, self._rowNum+1):
			self._printRow(rowIdx)

if __name__ == '__main__':

	kukuMulTable = MulTable()
	kukuMulTable.show()
