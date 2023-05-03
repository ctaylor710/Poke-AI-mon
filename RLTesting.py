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

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()
database.addStat()


def RobotAction(QFunction, pokemon, ally, opposingSide, field):
	# Create Action space out of pokemon.moves and ally.moves
	# Load statistics to determine most 5 (?) most likely pokemon sets
	# Use MaxDamageAI to predict human actions based on given guesses, feed into QFunction to create array
	# Select 5 best actions to take for each of the 5 sets
	# If at least one action is found in every list of 5 robot actions, choose the best average one
	# Else, use risk averse control by looking at each set and select the one that has the lowest average reward. Select the best reward from that.
	pass

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

	state = StateVector(myField, myField.userSide.pokes, myField.opponentSide.pokes)
	POField = field()
	POField.opponentSide.pokes[0] = opponentTeam[opponentPokes[0]]
	POField.opponentSide.pokes[1] = opponentTeam[opponentPokes[1]]
	POField.opponentSide.side = 'opponent'
	POField.opponentSide.availablePokes[0] = opponentTeam[opponentPokes[2]]
	POField.opponentSide.availablePokes[1] = opponentTeam[opponentPokes[3]]

	userPoke1 = pokemon()
	userPoke1.name = userTeam[userPokes[0]].name
	userPoke1.moves = [pokeMove(), pokeMove(), pokeMove(), pokeMove()]
	userPoke2 = pokemon()
	userPoke2.name = userTeam[userPokes[0]].name
	userPoke2.moves = [pokeMove(), pokeMove(), pokeMove(), pokeMove()]
	POField.userSide.pokes[0] = userPoke1
	POField.userSide.pokes[1] = userPoke2
	POField.userSide.side = 'user'

	# Load Q-Function here

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

		print(myField.userSide.pokes[0].name.name, myField.userSide.pokes[0].currHP)
		print(myField.userSide.pokes[1].name.name, myField.userSide.pokes[1].currHP)
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

		robotMoves, robotTargets = RobotAction(QFunction, POField.opponentSide.pokes[0], POField.opponentSide.pokes[0], POField.userSide, POField)
		moves = moves+robotMoves
		targets = targets+robotTargets

		action = env.TakeAction(myField, pokes, moves, targets, availablePokes, False)
		actions.append(str(action))

		state, myField = env.Dynamics(state, myField, pokes, moves, targets, availablePokes)
		states.append(str(state))
		POField = UpdateRobotKnowledge(state, moves, myField)

	if env.KOed(myField.opponentSide):
		print('You beat the robot, congratulations!')
	else:
		print('The robot was able to beat you.')
	return states, actions

Battle()