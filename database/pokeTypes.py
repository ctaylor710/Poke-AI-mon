class pokeType:
	def __init__(self):
		self.type = 'None'
		self.effectiveness = {}

	def addData(self, line):
		none = line.find('???')
		Normal = line.find('Normal')
		Grass = line.find('Grass')
		Fire = line.find('Fire')
		Water = line.find('Water')
		Electric = line.find('Electric')
		Ice = line.find('Ice')
		Flying = line.find('Flying')
		Bug = line.find('Bug')
		Poison = line.find('Poison')
		Ground = line.find('Ground')
		Rock = line.find('Rock')
		Fighting = line.find('Fighting')
		Psychic = line.find('Psychic')
		Dark = line.find('Dark')
		Steel = line.find('Steel')
		Ghost = line.find('Ghost')
		Dragon = line.find('Dragon')
		Fairy = line.find('Fairy')

		if none != -1:
			endIndex = line.find(',', none)
			splitLine = line[none:endIndex].split(':')
			splitLine[0] = 'None'
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Normal != -1:
			endIndex = line.find(',', Normal)
			splitLine = line[Normal:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Grass != -1:
			endIndex = line.find(',', Grass)
			splitLine = line[Grass:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Fire != -1:
			endIndex = line.find(',', Fire)
			splitLine = line[Fire:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Water != -1:
			endIndex = line.find(',', Water)
			splitLine = line[Water:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Electric != -1:
			endIndex = line.find(',', Electric)
			splitLine = line[Electric:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Ice != -1:
			endIndex = line.find(',', Ice)
			splitLine = line[Ice:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Flying != -1:
			endIndex = line.find(',', Flying)
			splitLine = line[Flying:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Bug != -1:
			endIndex = line.find(',', Bug)
			splitLine = line[Bug:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Poison != -1:
			endIndex = line.find(',', Poison)
			splitLine = line[Poison:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Ground != -1:
			endIndex = line.find(',', Ground)
			splitLine = line[Ground:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Rock != -1:
			endIndex = line.find(',', Rock)
			splitLine = line[Rock:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Fighting != -1:
			endIndex = line.find(',', Fighting)
			splitLine = line[Fighting:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Psychic != -1:
			endIndex = line.find(',', Psychic)
			splitLine = line[Psychic:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Dark != -1:
			endIndex = line.find(',', Dark)
			splitLine = line[Dark:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Steel != -1:
			endIndex = line.find(',', Steel)
			splitLine = line[Steel:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip().replace('}', ''))
		if Ghost != -1:
			endIndex = line.find(',', Ghost)
			splitLine = line[Ghost:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Dragon != -1:
			endIndex = line.find(',', Dragon)
			splitLine = line[Dragon:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip())
		if Fairy != -1:
			endIndex = line.find(',', Fairy)
			splitLine = line[Fairy:endIndex].split(':')
			if len(splitLine[1].strip()) > 0:
				self.effectiveness[splitLine[0]] = float(splitLine[1].strip().replace('}', ''))

	def __str__(self):
		types = list(self.effectiveness.keys())
		str=f'Attacker: {self.type}\nEffectiveness: {self.effectiveness}'
		return str
