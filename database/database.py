"""
This script compiles the complete list of Pokemon species, moves, types, and natures.
The data used to create this list can be found here: https://github.com/smogon/damage-calc/tree/master/calc/src/data
 *This repository is a reputable resource in the Pokemon community that provides accurate battle data that can
  be used for damage calculations under any battle state.
The data from this source is reformatted and compiled into dictionaries. These dictionaries will provide our robot with
a complete knowledge of fundamentals of Pokemon that can be used for damage calculations.

"""
from database.moves import move
from database.pokeTypes import pokeType
from database.species import species
from database.natures import nature

class database:

	def __init__(self):
		self.name = species()
		self.movesDict = {}
		self.typesDict = {}
		self.speciesDict = {}
		self.naturesDict = {}

	def addMoves(self):
		movesFile = open("database/moves.txt", "r")
		for line in movesFile:
			line = line.strip()
			if len(line) > 0:
				if line[0] == '\'':
					colonIndex = line.find(':')
					newMove = move()
					newMove.name = line[1:colonIndex-1]
					if newMove.name in self.movesDict.keys():
						newMove = self.movesDict[newMove.name]
					if line.find('}') != -1:
						newMove.addData(line)

					else:
						while line[0] != '}':
							newMove.addData(line)
							line = next(movesFile)

					self.movesDict[newMove.name] = newMove
		movesFile.close()

	def addTypes(self):
		typesFile = open("database/types.txt", "r")
		for line in typesFile:
			line = line.strip()
			if len(line) > 0:
				if line.find('{') != -1:
					endIndex = line.find(':')
					newType = pokeType()
					newType.type = line[0:endIndex]
					if newType.type == '\'???\'':
						newType.type = 'None'
					if newType.type in self.typesDict.keys():
						newType = self.typesDict[newType.type]
					self.typesDict[line[0:endIndex]] = newType
				if line.find('}') == -1:
					newType.addData(line)
				else:
					newType.addData(line[endIndex:])
					self.typesDict[newType.type] = newType
		typesFile.close()

	def addSpecies(self):
		speciesFile = open("database/species.txt", "r")
		for line in speciesFile:
			line = line.strip()
			if len(line) > 0:
				if line[0] == '\'':
					colonIndex = line.find(':')
					newSpecies = species()
					newSpecies.name = line[1:colonIndex-1]
					if newSpecies.name in self.speciesDict.keys():
						newSpecies = self.speciesDict[newSpecies.name]
					if line.find('}') != -1:
						newSpecies.addData(line)

					else:
						while line[0] != '}':
							newSpecies.addData(line)
							line = next(speciesFile)

					self.speciesDict[newSpecies.name] = newSpecies
		speciesFile.close()

	def addNatures(self):
		naturesFile = open("database/natures.txt", "r")
		for line in naturesFile:
			line = line.strip()
			if(len(line) > 0):
				newNature = nature()
				nameEndIndex = line.find(':')
				newNature.name = line[:nameEndIndex]
				newNature.addData(line)
				self.naturesDict[newNature.name] = newNature
		naturesFile.close()
