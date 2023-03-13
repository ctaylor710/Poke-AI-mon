class nature:
	def __init__(self):
		self.name = 'None'
		self.boost = 'None'
		self.lower = 'None'

	def addData(self, line):
		startIndex = line.find('[')
		endIndex = line.find(']')
		tempLine = line[startIndex+1:endIndex].replace('\'', '')
		tempList = tempLine.split(',')
		self.boost = tempList[0]
		self.lower = tempList[1]
	def __str__(self):
		str=f'Name: {self.name}\nBoosted Stat: {self.boost}\nLowered Stat: {self.lower}\n'
		return str
