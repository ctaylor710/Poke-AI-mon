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
import demonstration as dem

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()

file = open("DemonstrationData.txt", "r")

def ActionSpace(userPoke, ally, opponent, opponent2, availablePokes, field):
	actions = []

	pokes = [userPoke, ally, opponent, opponent2]
	repeat = True
	moves = []
	targets = []
	
	for move1 in userPoke.moves + ['switch']:
		# target 1 store the index of all possible target for user pokemon
		# print(move1)
		if move1 == 'switch':
			if len(availablePokes) == 2:
				target1 = [[0,5],[0,6]]
			elif len(availablePokes) == 1:
				target1 = [[0,5]]
			elif len(availablePokes) == 0:
				target1 = []
		else:
			if move1.target == 'Adjacent':
				target1 = [[2],[3],[4]]
			elif move1.target == 'AllAdjacentFoes':
				target1 = [[3, 4]]
			elif move1.target == 'AllAdjacent':
				target1 = [[2, 3, 4]]
			elif move1.target == 'Self':
				target1 = [[1]]

		for move2 in ally.moves + ['switch']:
			if move2 == 'switch':
				if len(availablePokes) == 2:
					target2 = [[0,5],[0,6]]
				elif len(availablePokes) == 1:
					target2 = [[0,5]]
				elif len(availablePokes) == 0:
					target2 = []
			else:
				# target 2 store the index of all possible target for ally pokemon
				if move2.target == 'Adjacent':
					target2 = [[1],[3],[4]]
				elif move2.target == 'AllAdjacentFoes':
					target2 = [[3, 4]]
				elif move2.target == 'AllAdjacent':
					target2 = [[1, 3, 4]]
				elif move2.target == 'Self':
					target2 = [[2]]

			for move3 in opponent.moves:
				# target 3 store the index of all possible target for opponent pokemon 1
				if move3.target == 'Adjacent':
					target3 = [[1],[2],[4]]
				elif move3.target == 'AllAdjacentFoes':
					target3 = [[1, 2]]
				elif move3.target == 'AllAdjacent':
					target3 = [[1, 2, 4]]
				elif move3.target == 'Self':
					target3 = [[3]]

				for move4 in opponent2.moves:
					# target 3 store the index of all possible target for opponent pokemon 2
					if move4.target == 'Adjacent':
						target4 = [[1],[2],[3]]
					elif move4.target == 'AllAdjacentFoes':
						target4 = [[1, 2]]
					elif move4.target == 'AllAdjacent':
						target4 = [[1, 2, 3]]
					elif move4.target == 'Self':
						target4 = [[4]]
				
				# Store every possible moves and target into a list
					for t1 in target1:
						for t2 in target2:
							for t3 in target3:
								for t4 in target4:
									moves.append([move1, move2, move3, move4])
									targets.append([t1, t2, t3, t4])


	for i in range(len(moves)):
		# take action with moves[i], targets[i]
		# append to actions
		move_temp = moves[i]
		target_temp = targets[i]
		action_temp = env.TakeAction(field, pokes, move_temp, target_temp, availablePokes, repeat)
		actions.append(action_temp)

	return actions

myField = field()
userTeam, opponentTeam = env.CreateEnv()

userPokes = random.sample(range(6), 4)
myField.userSide.pokes[0] = userTeam[userPokes[0]]
myField.userSide.pokes[1] = userTeam[userPokes[1]]
myField.userSide.side = 'user'
myField.userSide.availablePokes[0] = userTeam[userPokes[2]]
myField.userSide.availablePokes[1] = userTeam[userPokes[3]]

opponentPokes = random.sample(range(6), 4)
myField.opponentSide.pokes[0] = opponentTeam[opponentPokes[0]]
myField.opponentSide.pokes[1] = opponentTeam[opponentPokes[1]]
myField.opponentSide.side = 'opponent'
myField.opponentSide.availablePokes[0] = opponentTeam[opponentPokes[2]]
myField.opponentSide.availablePokes[1] = opponentTeam[opponentPokes[3]]

aSpace = ActionSpace(myField.userSide.pokes[0], myField.userSide.pokes[1], myField.opponentSide.pokes[0], myField.opponentSide.pokes[1], myField.userSide.availablePokes, myField)

print(aSpace[0])
