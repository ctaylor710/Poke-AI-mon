from database.database import database
from database.moves import move
from database.pokeTypes import pokeType
from database.species import species
from database.natures import nature
from pokemon import pokemon
from field import field
from side import side
from result import result
import utils
import damageCalc
import numpy as np
import random
import environment as env

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()

file = open("DemonstrationData.txt", "r")

def ActionSpace(userPoke, ally, opponent, opponent2, availablePokes, field):
	actions = []

	pokes = [userPoke, ally, opponent, opponent2]
	repeat = False
	moves = []
	targets = []
	for move1 in userPoke.moves:
		if move1.target == 'Adjacent':
			target1 = [[2],[3],[4]]
		elif move1.target == 'AllAdjacentFoes':
			target1 = [[3, 4]]
		elif move1.target == 'AllAdjacent':
			target1 = [[2, 3, 4]]
		elif move1.target == 'Self':
			target1 = [[1]]
		for move2 in ally.moves:
			for move3 in opponent.moves:
				for move4 in opponent2.moves:
					for t1 in target1:
						for t2 in target2:
							for t3 in target3:
								for t4 in target4:
									moves.append([move1, move2, move3, move4])
									targets.append([t1, t2, t3, t4])


	for i in range(len(moves)):
		# take action with moves[i], targets[i]
		# append to actions

	return actions
