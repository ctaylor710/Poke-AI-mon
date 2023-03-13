class species:
	def __init__(self):
		self.name = 'None'
		self.types = []
		self.bs = {}
		self.weightkg = 0
		self.gender = 'M/F'
		self.abilities = []
		self.baseSpecies = 'None'
		self.nfe = False
		self.statNames = ['hp', 'at', 'df', 'sa', 'sd', 'sp']
		

	def addData(self, line):
		types = line.find('types')
		bs = line.find('bs:')
		weightkg = line.find('weightkg')
		gender = line.find('gender')
		abilities = line.find('abilities')
		baseSpecies = line.find('baseSpecies')
		nfe = line.find('nfe')

		if types != -1:
			startIndex = line.find(':', types)
			endIndex = line.find(']', startIndex)
			tempLine = line[startIndex+1:endIndex].strip().replace('[', '')
			tempLine = tempLine.strip().replace(']', '')
			tempLine = tempLine.strip().replace('\'', '')
			tempList = tempLine.split(',')
			tempList = [tempList[i].strip() for i in range(len(tempList))]
			self.types = tempList

		if bs != -1:
			startIndex = line.find('{', bs)
			endIndex = line.find('}', startIndex)
			tempLine = line[startIndex+1:endIndex].strip().replace('{', '')
			tempLine = tempLine.strip().replace('}', '')
			tempLine = tempLine.strip().replace('\'', '')
			statList = tempLine.split(',')
			statDict = self.bs
			for i in range(len(statList)):
				pair = statList[i].strip().split(':')
				if pair[0] in self.statNames:
					statDict[pair[0]] = int(pair[1])
			self.bs = statDict

		if weightkg != -1:
			startIndex = line.find(':', weightkg)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.weightkg = float(line[startIndex+1:endIndex].strip())

		if gender != -1:
			startIndex = line.find(':', gender)
			endIndex = line.find(',', startIndex)
			self.gender = line[startIndex+1:endIndex].strip().replace('\'', '')

		if abilities != -1:
			startIndex = line.find('\'', abilities)
			endIndex = line.find('\'', startIndex+1)
			self.abilities = line[startIndex+1:endIndex]

		if baseSpecies != -1:
			startIndex = line.find(':', baseSpecies)
			endIndex = line.find(',', startIndex)
			self.baseSpecies = line[startIndex+1:endIndex].strip().replace('\'', '')

		if nfe != -1:
			self.nfe = True if ~self.nfe else False


	def __str__(self):
		str=f'Species: {self.name}\nTypes: {self.types}\nBase Stats: {self.bs}\nWeight (kg): {self.weightkg}\nGender: {self.gender}\n'
		str+=f'Abilities: {self.abilities}\nBase Species: {self.baseSpecies}\nNot Fully Evolved: {self.nfe}\n'
		return str
