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
import pickle
import environment as env


def RobotAction(pokemon, ally, opposingSide, field):
	

def Battle():
	myField = field()
	userTeam, opponentTeam = CreateEnv()
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

	# Load Q-Function here

	pokes = myField.userSide.pokes + myField.opponentSide.pokes
	availablePokes = myField.userSide.availablePokes + myField.opponentSide.availablePokes
	print(f'In back mons: {myField.userSide.availablePokes[0].name.name}, {myField.userSide.availablePokes[1].name.name}')
	while not (KOed(myField.userSide) or KOed(myField.opponentSide)):
		print('User Pokemon #1: ')
		print(myField.userSide.pokes[0])
		print('User Pokemon #2: ')
		print(myField.userSide.pokes[1])
		print('Opponent Pokemon #1: ')
		print(myField.opponentSide.pokes[0])
		print('Opponent Pokemon #2: ')
		print(myField.opponentSide.pokes[1])

		print(myField.userSide.pokes[0].name.name, myField.userSide.pokes[0].currHP)
		print(myField.userSide.pokes[1].name.name, myField.userSide.pokes[1].currHP)
		print(myField.opponentSide.pokes[0].name.name, myField.opponentSide.pokes[0].currHP)
		print(myField.opponentSide.pokes[1].name.name, myField.opponentSide.pokes[1].currHP)
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

		for i in range(len(myField.opponentSide.pokes)):
			ally = myField.opponentSide.pokes[1] if i == 0 else myField.opponentSide.pokes[0]
			move, target = RobotAction(QFunction, myField.opponentSide.pokes[i], ally, myField.userSide, myField)
			moves.append(move)
			targets.append(target)

		action = TakeAction(myField, pokes, moves, targets, availablePokes, False)
		actions.append(str(action))

		state, myField = Dynamics(state, myField, pokes, moves, targets, availablePokes)
		states.append(str(state))
	if KOed(myField.opponentSide):
		print('You beat the robot, congratulations!')
	else:
		print('The robot was able to beat you.')
	return states, actions
