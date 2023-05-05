from database.moves import move as pokeMove
from database.pokeTypes import pokeType
from database.species import species
from database.natures import nature
from database.database import database
from database.statistics import statistics
from pokemon import pokemon
from field import field
from side import side
from result import result
import utils
import damageCalc
import numpy as np
import random
import pickle
import environment as env
import torch
from actionSpace import ActionSpaceBot
import math
import RL
from singleVec import *
from dqn import DQN

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()
database.addStat()
opponentAI = torch.load('localQNetwork.pth')

def ApplyPokemonSet(poke, pokeSet):
	sets = []
	for i in range(10):
		newGuess = pokemon()
		newGuess.name = poke.name
		items = pokeSet[0].keys(); itemProbs = [pokeSet[0][i] for i in items]
		abilities = pokeSet[1].keys(); abilityProbs = [pokeSet[1][i] for i in abilities]
		moves = pokeSet[2].keys(); moveProbs = [pokeSet[2][i] for i in moves]
		stats = pokeSet[3].keys(); statProbs = [pokeSet[3][i] for i in stats]

		itemGuess = 'Other'
		while itemGuess == 'Other':
			if np.sum(itemProbs) != 1:
				itemProbs[-1] += 1-np.sum(itemProbs)
			itemGuess = list(items)[np.random.choice(range(len(items)), p=itemProbs)]
			newGuess.item = itemGuess

		if np.sum(abilityProbs) != 1:
			abilityProbs[-1] += 1-np.sum(abilityProbs)
		newGuess.ability = list(abilities)[np.random.choice(range(len(abilities)), p=abilityProbs)]

		moveProbs = [moveProbs[i]/np.sum(moveProbs) for i in range(len(moveProbs))]
		while len(newGuess.moves) < 4:
			newMove = list(moves)[np.random.choice(range(len(moves)), p=moveProbs)]
			if all(newMove != newGuess.moves[j].name for j in range(len(newGuess.moves))) and newMove != 'Other' and newMove != 'Perish Song' and newMove != 'Trick Room':
				newGuess.moves.append(database.movesDict[newMove])

		if np.sum(statProbs) != 1:
			statProbs[-1] += 1-np.sum(statProbs)
		while newGuess.nature.name == 'None':
			selectedSpread = list(stats)[np.random.choice(range(len(stats)), p=statProbs)]
			splitArr = selectedSpread.split(':')
			newGuess.addDataLine(database, splitArr[0]) # Easy way to add nature and nature boosts in one line
			if len(splitArr) > 1:
				EVs = splitArr[1].split('/')
				newGuess.EVs['hp'] = int(EVs[0]); newGuess.EVs['at'] = int(EVs[1]); newGuess.EVs['df'] = int(EVs[2]); newGuess.EVs['sa'] = int(EVs[3]); newGuess.EVs['sd'] = int(EVs[4]); newGuess.EVs['sp'] = int(EVs[5]);
				for stat in newGuess.name.bs.keys():
					if stat == 'hp':
						newGuess.stats[stat] = math.floor( ( math.floor( ((2*newGuess.name.bs[stat] + newGuess.IVs[stat] + math.floor(newGuess.EVs[stat]/4)) * \
							newGuess.level) / 100) ) + newGuess.level + 10)
						newGuess.currHP = newGuess.stats[stat]
					else:
						newGuess.stats[stat] = math.floor( ( math.floor( ((2*newGuess.name.bs[stat] + newGuess.IVs[stat] + math.floor(newGuess.EVs[stat]/4)) * \
							newGuess.level) / 100) + 5) * newGuess.natureBoosts[stat])

				newGuess.rawStats = newGuess.stats.copy()

		sets.append(newGuess)
	return sets


def RobotAction(userPoke, ally, opposingSide, poke1HPPercent, poke2HPPercent, field):
	actions = ActionSpaceBot(userPoke, ally, field.userSide.availablePokes, field)
	poke1Probs = database.statsDict[opposingSide.pokes[0].name.name]
	poke2Probs = database.statsDict[opposingSide.pokes[1].name.name]
	poke1Items = poke1Probs.ItemDic; poke2Items = poke2Probs.ItemDic
	poke1Abilities = poke1Probs.AbiDic; poke2Abilities = poke2Probs.AbiDic
	poke1Moves = poke1Probs.MoveDic; poke2Moves = poke2Probs.MoveDic
	poke1Stats = poke1Probs.SpreadDic; poke2Stats = poke2Probs.SpreadDic
	poke1Sets = [poke1Items, poke1Abilities, poke1Moves, poke1Stats]; poke2Sets = [poke2Items, poke2Abilities, poke2Moves, poke2Stats]
	poke1Guesses = ApplyPokemonSet(opposingSide.pokes[0], poke1Sets)
	poke2Guesses = ApplyPokemonSet(opposingSide.pokes[1], poke2Sets)
	botMoves = []; botTargets = []; avgRewards = []
	robotMove = []; robotTarget = []
	for i in range(len(poke1Guesses)):
		sampleField = field
		sampleField.opponentSide.pokes[0] = poke1Guesses[i]
		sampleField.opponentSide.pokes[0].currHP = poke1HPPercent*sampleField.opponentSide.pokes[0].rawStats['hp']
		sampleField.opponentSide.pokes[1] = poke2Guesses[i]
		sampleField.opponentSide.pokes[1].currHP = poke2HPPercent*sampleField.opponentSide.pokes[1].rawStats['hp']
		# print(sampleField.opponentSide.pokes[0])
		# print(sampleField.opponentSide.pokes[1])
		
		state = env.StateVector(sampleField, sampleField.userSide.pokes, sampleField.opponentSide.pokes)
		HA = RL.getHumanAction(sampleField)
		stateOne = rework(state)
		if len(stateOne) < 518:
			print(state[0])
			print(state[1])
		HAOne = rework(HA)
		state_size = 518
		HA_size = 318
		action_size = 194
		agent = DQN(state_size, HA_size, action_size)
		agent.qnetwork_local = opponentAI
		N = 5
		robotIndices, rewards = agent.Robot_action_N(stateOne, HAOne, N)
		avgRewards.append(np.average(rewards))
		# print('indices', robotIndices)
		sampleBotMoves = []; sampleBotTargets = []
		for j in range(N):
			move, target = RL.botChoose(sampleField, robotIndices[j])
			sampleBotMoves.append(move); sampleBotTargets.append(target)
		botMoves.append(sampleBotMoves)
		botTargets.append(sampleBotTargets)
	for i in range(len(botMoves[0])):
		count = 0
		for j in range(len(botMoves)):
			if botMoves[0][i] in botMoves[j]:
				count += 1
		if count >= N:
			robotMove = botMoves[0][i]
			robotTarget = botTargets[0][i]
	if len(robotMove) == 0:
		minIndex = np.argmin(avgRewards)
		robotMove = botMoves[minIndex][0]
		robotTarget = botTargets[minIndex][0]
	# [print(robotMove[i]) for i in range(2)]
	# print('before', robotTarget)
	for i in range(len(robotTarget)):
		for j in range(len(robotTarget[i])):
			if robotTarget[i][j] in [1, 2, 5, 6]:
				robotTarget[i][j] += 2
			elif robotTarget[i][j] in [3, 4]:
				robotTarget[i][j] -= 2

	# print('after', robotTarget)
	return robotMove, robotTarget


	# Load statistics to determine most 5 (?) most likely pokemon sets
	# Use MaxDamageAI to predict human actions based on given guesses, feed into QFunction to create array
	# Select 5 best actions to take for each of the 5 sets
	# If at least one action is found in every list of 5 robot actions, choose the best average one
	# Else, use risk averse control by looking at each set and select the one that has the lowest average reward. Select the best reward from that.
	

def UpdateRobotKnowledge(state, moves, targets, field):

	POField = field()

	# Update known moves
	for i in range(2):
		for j in range(4):
			if POield.userSide.pokes[i].moves[j].name == 'None':
				if moves[i] != 'switch':
					POfield.userSide.pokes[i].moves[j] = moves[i]
					for t in targets[i]:
						if (t == 3 or t == 4) and moves[i]:
							POResult = result()
							POResult = damageCalc.TakeMove(POField.userSide.pokes[i], 'user', POField.opponentSide.pokes[t-3], 'opponent', moves[i], POField, t, POResult)
							if t == 3:
								predictedDamage = POResult.opponentDamage
							else:
								predictedDamage = POResult.opponent2Damage

					break

	# Update field knowledge
	POField.weather = field.weather
	POField.terrain = field.terrain
	POField.trickRoom = field.trickRoom
	POField.trickRoomTurns = field.trickRoomTurns
	POField.isBeadsOfRuin = field.isBeadsOfRuin
	POField.isSwordOfRuin = field.isSwordOfRuin
	POField.isTabletsOfRuin = field.isTabletsOfRuin
	POField.isVesselOfRuin = field.isVesselOfRuin

	# Update side knowledge
	POField.opponentSide = field.opponentSide
	POField.userSide.isReflect = field.userSide.isReflect
	POField.userSide.reflectTurns = field.userSide.reflectTurns
	POField.userSide.isLightScreen = field.userSide.isLightScreen
	POField.userSide.lightScreenTurns = field.userSide.lightScreenTurns
	POField.userSide.tailwind = field.userSide.tailwind
	POField.userSide.tailwindTurns = field.userSide.tailwindTurns
	POField.userSide.isAuroraVeil = field.userSide.isAuroraVeil
	POField.userSide.auroraVeilTurns = field.userSide.auroraVeilTurns


def Battle():
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

	state = env.StateVector(myField, myField.userSide.pokes, myField.opponentSide.pokes)
	POField = field()
	POField.userSide.pokes[0] = opponentTeam[opponentPokes[0]]
	POField.userSide.pokes[1] = opponentTeam[opponentPokes[1]]
	POField.userSide.side = 'opponent'
	POField.userSide.availablePokes[0] = opponentTeam[opponentPokes[2]]
	POField.userSide.availablePokes[1] = opponentTeam[opponentPokes[3]]

	oppPoke1 = pokemon()
	oppPoke1.name = userTeam[userPokes[0]].name
	oppPoke1.moves = [pokeMove(), pokeMove(), pokeMove(), pokeMove()]
	oppPoke2 = pokemon()
	oppPoke2.name = userTeam[userPokes[1]].name
	oppPoke2.moves = [pokeMove(), pokeMove(), pokeMove(), pokeMove()]
	POField.opponentSide.pokes[0] = oppPoke1
	POField.opponentSide.pokes[1] = oppPoke2
	POField.opponentSide.side = 'opponent'

	pokes = myField.userSide.pokes + myField.opponentSide.pokes
	availablePokes = myField.userSide.availablePokes + myField.opponentSide.availablePokes
	print(f'In back mons: {myField.userSide.availablePokes[0].name.name}, {myField.userSide.availablePokes[1].name.name}')
	while not (env.KOed(myField.userSide) or env.KOed(myField.opponentSide)):
		print('User Pokemon #1: ')
		print(myField.userSide.pokes[0])
		print('User Pokemon #2: ')
		print(myField.userSide.pokes[1])
		print('Opponent Pokemon #1: ')
		print(myField.opponentSide.pokes[0].name.name)
		print('Opponent Pokemon #2: ')
		print(myField.opponentSide.pokes[1].name.name)

		print('User Pokemon HP')
		print(myField.userSide.pokes[0].name.name, myField.userSide.pokes[0].currHP)
		print(myField.userSide.pokes[1].name.name, myField.userSide.pokes[1].currHP)
		print('Opponent Pokemon HP Percentage')
		print(myField.opponentSide.pokes[0].name.name, max(1, 100*round(myField.opponentSide.pokes[0].currHP/myField.opponentSide.pokes[0].rawStats['hp'], 2)), '%')
		print(myField.opponentSide.pokes[1].name.name, max(1, 100*round(myField.opponentSide.pokes[1].currHP/myField.opponentSide.pokes[1].rawStats['hp'], 2)), '%')
		moves = []
		targets = []
		for i in range(len(myField.userSide.pokes)):
			move = input('Which move will you take? ')
			target = input('Who are you targeting? ')
			target = target.split(',')
			target = [int(target[i].strip()) for i in range(len(target))]
			if move == 'switch':
				moves.append(move)
			else:
				moves.append(database.movesDict[move])
			targets.append(target)

		userPoke1Percentage = max(1, round(myField.userSide.pokes[0].currHP/myField.userSide.pokes[0].rawStats['hp']))
		userPoke2Percentage = max(1, round(myField.userSide.pokes[1].currHP/myField.userSide.pokes[1].rawStats['hp']))
		robotMoves, robotTargets = RobotAction(POField.userSide.pokes[0], POField.userSide.pokes[1], \
			POField.opponentSide, userPoke1Percentage, userPoke2Percentage, POField)
		moves = moves+robotMoves
		targets = targets+robotTargets
		# print(moves)
		# print(targets)

		# action = env.TakeAction(myField, pokes, moves, targets, availablePokes, False)
		# actions.append(str(action))
		# print(action)
		state, myField = env.Dynamics(state, myField, pokes, moves, targets, availablePokes)
		# print(myField.opponentSide.pokes[0].currHP, myField.opponentSide.pokes[0].rawStats['hp'])
		# print(myField.opponentSide.pokes[1].currHP)
		# states.append(str(state))
		# POField = UpdateRobotKnowledge(state, moves, myField)

	if env.KOed(myField.opponentSide):
		print('You beat the robot, congratulations!')
	else:
		print('The robot was able to beat you.')
	return states, actions

Battle()