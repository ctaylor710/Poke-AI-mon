class statistics:
	def __init__(self):
		self.name='None'
		# All the dictionary attributes
		self.AbiDic = {}
		self.ItemDic = {}
		self.MoveDic = {}
		self.SpreadDic = {}
		# All the flag attributes, initialize them as False
		self.AbiFlag= False
		self.ItemFlag = False
		self.MoveFlag = False
		self.SpreadFlag = False
			
	def addData(self,line):
		# Get the location of the specific word I am looking for
		AbiIdx = line.find('Abilities')
		ItemIdx = line.find('Items')
		MoveIdx = line.find('Moves')
		SpreadIdx = line.find('Spreads')
		# If the word is detected, change the flag to extract datas
		if AbiIdx != -1:
			self.AbiFlag = True
			self.ItemFlag = False
			self.MoveFlag = False
			self.SpreadFlag = False
		if ItemIdx != -1:
			self.AbiFlag = False
			self.ItemFlag = True
			self.MoveFlag = False
			self.SpreadFlag = False
		if MoveIdx != -1:
			self.AbiFlag = False
			self.ItemFlag = False
			self.MoveFlag = True
			self.SpreadFlag = False
		if SpreadIdx != -1:
			self.AbiFlag = False
			self.ItemFlag = False
			self.MoveFlag = False
			self.SpreadFlag = True
		# Storing the data in a dctionary
		if self.AbiFlag == True:
			startIndex = line.find('|')
			endIndex = line.find('+')
			tempLine = line[startIndex+1:endIndex].strip()
			if any(chr.isdigit() for chr in tempLine) == True:
				tempLine = tempLine.strip("%")
				tempLine = tempLine.split(" ")
				tempLine = [x for x in tempLine if x != '']
				key = ''
				item = 0
				for idx in range(len(tempLine)):
					valuecheck = '.'
					if idx == 0:
						key += tempLine[idx]
					elif valuecheck not in tempLine[idx] and idx != 0:
						tempLine[idx] = ' ' + tempLine[idx]
						key += tempLine[idx]
					else:
						item = round(float(tempLine[idx])/100,5)
				self.AbiDic[key] = item
				
		if self.ItemFlag == True:
			startIndex = line.find('|')
			endIndex = line.find('+')
			tempLine = line[startIndex+1:endIndex].strip()
			if any(chr.isdigit() for chr in tempLine) == True:
				tempLine = tempLine.strip("%")
				tempLine = tempLine.split(" ")
				tempLine = [x for x in tempLine if x != '']
				key = ''
				item = 0
				for idx in range(len(tempLine)):
					valuecheck = '.'
					if idx == 0:
						key += tempLine[idx]
					elif valuecheck not in tempLine[idx] and idx != 0:
						tempLine[idx] = ' ' + tempLine[idx]
						key += tempLine[idx]
					else:
						item = round(float(tempLine[idx])/100,5)
				self.ItemDic[key] = item
				
		if self.MoveFlag == True:
			startIndex = line.find('|')
			endIndex = line.find('+')
			tempLine = line[startIndex+1:endIndex].strip()
			if any(chr.isdigit() for chr in tempLine) == True:
				tempLine = tempLine.strip("%")
				tempLine = tempLine.split(" ")
				tempLine = [x for x in tempLine if x != '']
				key = ''
				item = 0
				for idx in range(len(tempLine)):
					valuecheck = '.'
					if idx == 0:
						key += tempLine[idx]
					elif valuecheck not in tempLine[idx] and idx != 0:
						tempLine[idx] = ' ' + tempLine[idx]
						key += tempLine[idx]
					else:
						item = round(float(tempLine[idx])/100,5)
				self.MoveDic[key] = item
				
		if self.SpreadFlag == True:
			startIndex = line.find('|')
			endIndex = line.find('+')
			tempLine = line[startIndex+1:endIndex].strip()
			if any(chr.isdigit() for chr in tempLine) == True:
				tempLine = tempLine.strip("%")
				tempLine = tempLine.split(" ")
				tempLine = [x for x in tempLine if x != '']
				key = ''
				item = 0
				for idx in range(len(tempLine)):
					valuecheck = '.'
					if idx == 0:
						key += tempLine[idx]
					elif valuecheck not in tempLine[idx] and idx != 0:
						tempLine[idx] = ' ' + tempLine[idx]
						key += tempLine[idx]
					else:
						item = round(float(tempLine[idx])/100,5)
				self.SpreadDic[key] = item
			
	def __str__(self):
		str = f'Species: {self.name}\nAbilities: {self.AbiDic}\nItems: {self.ItemDic}\n'
		str += f'Moves: {self.MoveDic}\nSpreads: {self.SpreadDic}\n'
		return str