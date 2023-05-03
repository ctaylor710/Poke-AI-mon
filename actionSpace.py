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


def ActionSpaceBot(userPoke, ally, availablePokes, field):
	actions = []

	pokes = [userPoke, ally]
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
				target1 = [[0,5], [0,5]]
			elif len(availablePokes) == 0:
				target1 = [[-1, -1], [-1, -1]]
		else:
			if move1.target == 'Adjacent':
				target1 = [[2],[3],[4]]
			elif move1.target == 'AllAdjacentFoes':
				target1 = [[3, 4], [3, 4], [3, 4]]
			elif move1.target == 'AllAdjacent':
				target1 = [[2, 3, 4], [2, 3, 4], [2, 3, 4]]
			elif move1.target == 'Self':
				target1 = [[1], [1], [1]]

		for move2 in ally.moves + ['switch']:
			if move2 == 'switch':
				if len(availablePokes) == 2:
					target2 = [[0,5],[0,6]]
				elif len(availablePokes) == 1:
					target2 = [[0,5], [0,5]]
				elif len(availablePokes) == 0:
					target2 = [[-1, -1], [-1, -1]]
			else:
				# target 2 store the index of all possible target for ally pokemon
				if move2.target == 'Adjacent':
					target2 = [[1],[3],[4]]
				elif move2.target == 'AllAdjacentFoes':
					target2 = [[3, 4], [3, 4], [3, 4]]
				elif move2.target == 'AllAdjacent':
					target2 = [[1, 3, 4], [1, 3, 4], [1, 3, 4]]
				elif move2.target == 'Self':
					target2 = [[2], [2], [2]]				
				# Store every possible moves and target into a list
			for t1 in target1:
				for t2 in target2:
					moves.append([move1, move2])
					targets.append([t1, t2])

	# for i in range(len(moves)):
	# 	# take action with moves[i], targets[i]
	# 	# append to actions
	# 	move_temp = moves[i]
	# 	target_temp = targets[i]
	# 	result_temp = damageCalc.TakeMove(attacker, attackerSide, defender, defenderSide, move, field, target, result)
	# 	# take move -> result
    #     # ActionVec(result) -> action vector
	# 	# action_temp = env.TakeAction(field, pokes, move_temp, target_temp, availablePokes, repeat)
	# 	actions.append(action_temp)
    #---------------------------------------------------------------------------------------------------------------------
    # We do not need it to return a full action list, because all we need is the pokemon's move and it's target

	return moves, targets

def ActionSpaceHuman (field):
	movesVec = []
	targetVec = []
	for i in range(2):
		move, target = env.maxDamageAI(field.opponentSide.pokes[i], field.opponentSide.pokes[-1*i + 1], field.userSide, field)
		movesVec.append(move)
		targetVec.append(target)
	return movesVec, targetVec
	





# myField = field()
# userTeam, opponentTeam = env.CreateEnv()

# userPokes = random.sample(range(6), 4)
# myField.userSide.pokes[0] = userTeam[userPokes[0]]
# myField.userSide.pokes[1] = userTeam[userPokes[1]]
# myField.userSide.side = 'user'
# myField.userSide.availablePokes[0] = userTeam[userPokes[2]]
# myField.userSide.availablePokes[1] = userTeam[userPokes[3]]

# opponentPokes = random.sample(range(6), 4)
# myField.opponentSide.pokes[0] = opponentTeam[opponentPokes[0]]
# myField.opponentSide.pokes[1] = opponentTeam[opponentPokes[1]]
# myField.opponentSide.side = 'opponent'
# myField.opponentSide.availablePokes[0] = opponentTeam[opponentPokes[2]]
# myField.opponentSide.availablePokes[1] = opponentTeam[opponentPokes[3]]


# movesBot, targetBot = ActionSpaceBot(myField.userSide.pokes[0], myField.userSide.pokes[1], myField.userSide.availablePokes, myField)
# movesHuman, targeHuman = ActionSpaceHuman(myField)
# # print(movesBot)
# # print(targetBot)
# # print(movesHuman)
# # print(targeHuman)

# testmove = movesBot[0] + movesHuman
# testtarget = targetBot[0] + targeHuman
# action = env.TakeAction(myField, myField.userSide.pokes + myField.opponentSide.pokes, testmove, testtarget, myField.userSide.availablePokes, True)
