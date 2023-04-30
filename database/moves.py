class move:
	def __init__(self):
		self.name = 'None'
		self.bp = 0
		self.zp = 0
		self.maxPower = 0
		self.type = 'Normal'
		self.category = 'Status'
		self.multihit = [1]
		self.hits = 1
		self.drain = 0
		self.recoil = 0
		self.mindBlownRecoil = False
		self.hasCrashDamage = False
		self.struggleRecoil = False
		self.priority = 0
		self.target = 'Adjacent'
		self.makesContact = False
		self.isPunch = False
		self.boosts = {}
		self.isSound = False
		self.isBullet = False
		self.isPulse = False
		self.isBite = False
		self.isZ = False
		self.isMax = False
		self.isWind = False
		self.isSlicing = False
		self.secondaries = False
		self.ignoreDefensive = False
		self.breaksProtect = False
		self.willCrit = False
		self.overrideOffensivePokemon = 'None'
		self.overrideDefensiveStat = 'None'
		self.overrideOffensiveStat = 'None'

		self.isCrit = False

	def addData(self, line):
		bp = line.find('bp')
		zp = line.find('zp')
		maxPower = line.find('maxPower')
		pokeType = line.find('type')
		category = line.find('category')
		multihit = line.find('multihit')
		drain = line.find('drain')
		recoil = line.find('recoil')
		mindBlownRecoil = line.find('mindBlownRecoil')
		hasCrashDamage = line.find('hasCrashDamage')
		struggleRecoil = line.find('struggleRecoil')
		priority = line.find('priority')
		target = line.find('target')
		makesContact = line.find('makesContact')
		isPunch = line.find('isPunch')
		boosts = line.find('boosts')
		isSound = line.find('isSound')
		isBullet = line.find('isBullet')
		isPulse = line.find('isPulse')
		isBite = line.find('isBite')
		isZ = line.find('isZ')
		isMax = line.find('isMax')
		isWind = line.find('isWind')
		isSlicing = line.find('isSlicing')
		secondaries = line.find('secondaries')
		ignoreDefensive = line.find('ignoreDefensive')
		breaksProtect = line.find('breaksProtect')
		willCrit = line.find('willCrit')
		overrideOffensivePokemon = line.find('overrideOffensivePokemon')
		overrideDefensiveStat = line.find('overrideDefensiveStat')
		overrideOffensiveStat = line.find('overrideOffensiveStat')

		if bp != -1:
			startIndex = line.find(':', bp)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.bp = int(line[startIndex+1:endIndex].strip())

		if zp != -1:
			startIndex = line.find(':', zp)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.zp = int(line[startIndex+1:endIndex].strip())

		if maxPower != -1:
			startIndex = line.find(':', maxPower)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.maxPower = int(line[startIndex+1:endIndex].strip())

		if pokeType != -1:
			startIndex = line.find(':', pokeType)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.type = line[startIndex+1:endIndex].strip().replace('\'', '')

		if category != -1:
			startIndex = line.find(':', category)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.category = line[startIndex+1:endIndex].strip().replace('\'', '')

		if multihit != -1:
			singleValue = False
			startIndex = line.find(':', multihit)
			endIndex = line.find(']', startIndex)
			if endIndex == -1:
				singleValue = True
				endIndex = line.find(',', startIndex)
				if line[endIndex-1] == '}':
					endIndex -= 1
			if ~singleValue:
				tempLine = line[startIndex+1:endIndex].strip().replace('[', '')
				tempLine = tempLine.strip().replace(']', '')
				self.multihit = list(map(int, tempLine.split(',')))
			else:
				self.multihit = line[startIndex+1:endIndex].strip()

		if drain != -1:
			singleValue = False
			startIndex = line.find(':', drain)
			endIndex = line.find(']', startIndex)
			if endIndex == -1:
				singleValue = True
				endIndex = line.find(',', startIndex)
				if line[endIndex-1] == '}':
					endIndex -= 1
			if ~singleValue:
				tempLine = line[startIndex+1:endIndex].strip().replace('[', '')
				tempLine = tempLine.strip().replace(']', '')
				self.drain = list(map(int, tempLine.split(',')))
				self.drain = self.drain[0]/self.drain[1]
			else:
				self.drain = int(line[startIndex+1:endIndex].strip())


		if recoil != -1:
			singleValue = False
			startIndex = line.find(':', recoil)
			endIndex = line.find(']', startIndex)
			if endIndex == -1:
				singleValue = True
				endIndex = line.find(',', startIndex)
				if line[endIndex-1] == '}':
					endIndex -= 1
			if ~singleValue:
				tempLine = line[startIndex+1:endIndex].strip().replace('[', '')
				tempLine = tempLine.strip().replace(']', '')
				self.recoil = list(map(int, tempLine.split(',')))
				self.recoil = self.recoil[0]/self.recoil[1]
			else:
				self.recoil = line[startIndex+1:endIndex].strip()

		if mindBlownRecoil != -1:
			self.mindBlownRecoil = False if self.mindBlownRecoil else True

		if hasCrashDamage != -1:
			self.hasCrashDamage = False if self.hasCrashDamage else True

		if struggleRecoil != -1:
			self.struggleRecoil = False if self.struggleRecoil else True

		if priority != -1:
			startIndex = line.find(':', priority)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.priority = int(line[startIndex+1:endIndex].strip())

		if target != -1:
			startIndex = line.find(':', target)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.target = line[startIndex+1:endIndex].strip().replace('\'', '')

		if makesContact != -1:
			self.makesContact = False if self.makesContact else True

		if isPunch != -1:
			self.isPunch = False if self.isPunch else True

		if boosts != -1:
			startIndex = line.find('{', boosts)
			endIndex = line.find('}', startIndex)
			tempLine = line[startIndex+1:endIndex].strip()
			tempList = tempLine.split(',')
			tempDict = {}
			for i in range(len(tempList)):
				pair = tempList[i].split(':')
				tempDict[pair[0]] = pair[1]
			self.boosts = tempDict

		if isSound != -1:
			self.isSound = False if self.isSound else True

		if isBullet != -1:
			self.isBullet = False if self.isBullet else True

		if isPulse != -1:
			self.isPulse = False if self.isPulse else True

		if isBite != -1:
			self.isPulse = False if self.isPulse else True

		if isZ != -1:
			self.isZ = False if self.isZ else True

		if isMax != -1:
			self.isMax = False if self.isMax else True

		if isWind != -1:
			self.isWind = False if self.isWind else True

		if isSlicing != -1:
			self.isSlicing = False if self.isSlicing else True

		if secondaries != -1:
			self.secondaries = False if self.secondaries else True

		if ignoreDefensive != -1:
			self.ignoreDefensive = False if self.ignoreDefensive else True

		if breaksProtect != -1:
			self.breaksProtect = False if self.breaksProtect else True

		if willCrit != -1:
			self.willCrit = False if self.willCrit else True
			if self.willCrit:
				self.isCrit = True

		if overrideOffensivePokemon != -1:
			startIndex = line.find(':', overrideOffensivePokemon)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.overrideOffensivePokemon = line[startIndex+1:endIndex].strip().replace('\'', '')

		if overrideDefensiveStat != -1:
			startIndex = line.find(':', overrideDefensiveStat)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.overrideDefensiveStat = line[startIndex+1:endIndex].strip().replace('\'', '')

		if overrideOffensiveStat != -1:
			startIndex = line.find(':', overrideOffensiveStat)
			endIndex = line.find(',', startIndex)
			if line[endIndex-1] == '}':
				endIndex -= 1
			self.overrideOffensiveStat = line[startIndex+1:endIndex].strip().replace('\'', '')



	def __str__(self):
		str=f'Name: {self.name}\nbp: {self.bp}\nzp: {self.zp}\nmaxPower: {self.maxPower}\nType: {self.type}\nCategory: {self.category}\n'
		str+=f'Multihit: {self.multihit}\nDrain: {self.drain}\nRecoil: {self.recoil}\nMind Blown Recoil: {self.mindBlownRecoil}\n'
		str+=f'Has Crash Damage: {self.hasCrashDamage}\nStruggle Recoil: {self.struggleRecoil}\nPriority: {self.priority}\n'
		str+=f'Target: {self.target}\nMakes Contact: {self.makesContact}\nPunching Move: {self.isPunch}\nBoosts: {self.boosts}\n'
		str+=f'Sound Move: {self.isSound}\nPulse Move: {self.isPulse}\nZ-Move: {self.isZ}\nDynamax Move: {self.isMax}\nWind Move: {self.isWind}\n'
		str+=f'Slicing Move: {self.isSlicing}\nSecondary Abilities: {self.secondaries}\nIgnores Defense: {self.ignoreDefensive}\n'
		str+=f'Breaks Protect: {self.breaksProtect}\nOverrides Offensive Pokemon: {self.overrideOffensivePokemon}\n'
		str+=f'Overriding Defensive Stat: {self.overrideDefensiveStat}\nOverriding Offensive Stat: {self.overrideOffensiveStat}\n'
		return str
