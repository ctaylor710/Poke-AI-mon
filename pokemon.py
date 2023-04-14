"""
-This class constructs a pokemon object, which is an object that contains all known information
about the pokemon. 
-To give this class the information needed to construct a pokemon object, the user
must feed the program the name of a text file containing the information of their pokemon. 
	-To build the text file, the user must create their pokemon here: https://play.pokemonshowdown.com/teambuilder
	-They will then click export and copy the data into their text file. 

"""
from database.database import database
from database.moves import move
from database.pokeTypes import pokeType
from database.species import species
from database.natures import nature
import math

class pokemon:
	def __init__(self):
		self.name = species()
		self.item = 'None'
		self.ability = 'None'
		self.abilityOn = False
		self.tera = 'None'
		self.isTera = False
		self.EVs = {'hp':0, 'at':0, 'df':0, 'sa':0, 'sd':0, 'sp':0}
		self.IVs = {'hp':31, 'at':31, 'df':31, 'sa':31, 'sd':31, 'sp':31}
		self.level = 50
		self.nature = nature()
		self.moves = []
		self.stats = self.name.bs
		self.rawStats = 0
		self.boosts = {'hp':0, 'at':0, 'df':0, 'sa':0, 'sd':0, 'sp':0}
		self.natureBoosts = {'hp':1, 'at':1, 'df':1, 'sa':1, 'sd':1, 'sp':1}
		self.status = 'Healthy'
		self.statusList = ['Healthy', 'Sleep', 'Poison', 'Burn', 'Frozen', 'Paralyze', 'Toxic']
		self.ignoresScreens = False
		self.currHP = 0
		self.alliesFainted = 0
		self.isSwitching = 'in' # None, in, out. We initialize each pokemon to 'in' for some checks that need to happen at beginnings of battles as well as when pokemon are switched in
		self.isEncored = False
		self.lastMove = move()
		self.isFollowMe = False


	def addData(self, database):
		fileName = input("Enter file containing pokemon information: ")
		readFile = open(f"pokemonFiles/{fileName}")
		for line in readFile:
			line = line.strip()
			if len(line) > 0:
				words = line.split(' ')
				pokeName = line.split('@')
				pokeName[0].strip()
				if pokeName[0] in database.speciesDict.keys():
					self.name = database.speciesDict[pokeName[0]]
					startIndex = line.find('@')
					if startIndex != -1:
						self.item = line[startIndex+1:].strip()
				if words[0] == 'Ability:':
					startIndex = line.find(':')
					self.ability = line[startIndex+1:].strip()
				if words[0] == 'Tera':
					startIndex = line.find(':')
					self.tera = line[startIndex+1:].strip()
				if words[0] == 'EVs:':
					hp = -1; at = -1; df = -1; sa = -1; sd = -1; sp = -1
					if 'HP' in words:
						hp = words.index('HP')
					if 'Atk' in words:
						at = words.index('Atk')
					if 'Def' in words:
						df = words.index('Def')
					if 'SpA' in words:
						sa = words.index('SpA')
					if 'SpD' in words:
						sd = words.index('SpD')
					if 'Spe' in words:
						sp = words.index('Spe')
					if hp != -1:
						self.EVs['hp'] = int(words[hp-1])
					if at != -1:
						self.EVs['at'] = int(words[at-1])
					if df != -1:
						self.EVs['df'] = int(words[df-1])
					if sa != -1:
						self.EVs['sa'] = int(words[sa-1])
					if sd != -1:
						self.EVs['sd'] = int(words[sd-1])
					if sp != -1:
						self.EVs['sp'] = int(words[sp-1])
				if words[0] in database.naturesDict.keys():
					self.nature = database.naturesDict[words[0]]
					self.natureBoosts[self.nature.boost] = 1.1
					self.natureBoosts[self.nature.lower] = 0.9
				if words[0] == '-':
					startIndex = 1
					if line[startIndex:].strip() in database.movesDict.keys():
						self.moves.append(database.movesDict[line[startIndex:].strip()])
					else:
						tempMove = move()
						move.name = line[startIndex:].strip()
						self.moves.append(tempMove)
					
		for stat in self.name.bs.keys():
			if stat == 'hp':
				self.stats[stat] = math.floor( ( math.floor( ((2*self.name.bs[stat] + self.IVs[stat] + math.floor(self.EVs[stat]/4)) * \
					self.level) / 100) ) + self.level + 10)
				self.currHP = self.stats[stat]
			else:
				self.stats[stat] = math.floor( ( math.floor( ((2*self.name.bs[stat] + self.IVs[stat] + math.floor(self.EVs[stat]/4)) * \
					self.level) / 100) + 5) * self.natureBoosts[stat])

		self.rawStats = self.stats.copy()

	def addDataLine(self, database, line):
		line = line.strip()
		if len(line) > 0:
			words = line.split(' ')
			pokeName = line.split('@')
			pokeName[0] = pokeName[0].strip()
			if pokeName[0] in database.speciesDict.keys():
				self.name = database.speciesDict[pokeName[0]]
				startIndex = line.find('@')
				if startIndex != -1:
					self.item = line[startIndex+1:].strip()
			if words[0] == 'Ability:':
				startIndex = line.find(':')
				self.ability = line[startIndex+1:].strip()
			if words[0] == 'Tera':
				startIndex = line.find(':')
				self.tera = line[startIndex+1:].strip()
			if words[0] == 'EVs:':
				hp = -1; at = -1; df = -1; sa = -1; sd = -1; sp = -1
				if 'HP' in words:
					hp = words.index('HP')
				if 'Atk' in words:
					at = words.index('Atk')
				if 'Def' in words:
					df = words.index('Def')
				if 'SpA' in words:
					sa = words.index('SpA')
				if 'SpD' in words:
					sd = words.index('SpD')
				if 'Spe' in words:
					sp = words.index('Spe')
				if hp != -1:
					self.EVs['hp'] = int(words[hp-1])
				if at != -1:
					self.EVs['at'] = int(words[at-1])
				if df != -1:
					self.EVs['df'] = int(words[df-1])
				if sa != -1:
					self.EVs['sa'] = int(words[sa-1])
				if sd != -1:
					self.EVs['sd'] = int(words[sd-1])
				if sp != -1:
					self.EVs['sp'] = int(words[sp-1])
			if words[0] in database.naturesDict.keys():
				self.nature = database.naturesDict[words[0]]
				self.natureBoosts[self.nature.boost] = 1.1
				self.natureBoosts[self.nature.lower] = 0.9
			if words[0] == '-':
				startIndex = 1
				if line[startIndex:].strip() in database.movesDict.keys():
					self.moves.append(database.movesDict[line[startIndex:].strip()])
				else:
					tempMove = move()
					move.name = line[startIndex:].strip()
					self.moves.append(tempMove)
				
		for stat in self.name.bs.keys():
			if stat == 'hp':
				self.stats[stat] = math.floor( ( math.floor( ((2*self.name.bs[stat] + self.IVs[stat] + math.floor(self.EVs[stat]/4)) * \
					self.level) / 100) ) + self.level + 10)
				self.currHP = self.stats[stat]
			else:
				self.stats[stat] = math.floor( ( math.floor( ((2*self.name.bs[stat] + self.IVs[stat] + math.floor(self.EVs[stat]/4)) * \
					self.level) / 100) + 5) * self.natureBoosts[stat])

		self.rawStats = self.stats.copy()

	def addBoosts(self, stat, amount):
		if amount > 0:
			self.boosts[stat] = min(self.boosts[stat] + amount, +6)
		else:
			self.boosts[stat] = max(self.boosts[stat] + amount, -6)

	def __str__(self):
		str=f'Pokemon: {self.name.name}\nItem: {self.item}\nAbility: {self.ability}\nTera type: {self.tera}\nEV Spread: {self.EVs}\n'
		str+=f'Nature: {self.nature.name}\nMoves: {self.moves[0].name}, {self.moves[1].name}, {self.moves[2].name}, {self.moves[3].name}'

		return str


