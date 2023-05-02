import numpy as np
import torch
from torch.optim import Adam
from DQN.memory import MyMemory
from DQN.dqn import DQN
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
from singleVec import *

# Initialize states
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

# This returns the predicted human action
def Human_action(field):
    actionVec = []
    # call the max damage ai to output the predicted move and it's target
    for i in range(2):
        move, target = env.maxDamageAI(field.opponentSide.pokes[i], field.opponentSide.pokes[-1*i + 1], field.userSide, field)
        moveResult = result()
        for t in target:
            moveResult = damageCalc.TakeMove(field.opponentSide.pokes[i], 'opponent', field.userSide.pokes[i], 'user', move, field, t, moveResult)
            action = env.actionVector(moveResult)
        # reward = env.RewardModel(state, action, theta)
        actionVec.append(action)
        # rewardVec.append(reward)
    # index = np.argmax(rewardVec)
    # HA =  actionVec[index]
    return(actionVec)

# HA = Human_action(myField)
# HA = rework(HA)
# print(len(HA))

r1 = [[3, 6, 131, 90, 134, 176, 81, 206, 0, 0, 0, 0, 0, 0, 131, 23, 181, 13, False, 0, 0, 0, 252, 4, 252, 31, 31, 31, 31, 31, 31, 1, 0.9, 1, 1, 1, 1.1, [70, 6, 2, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [55, 6, 2, [1], 0, 0, 0, 3, False, False, False, False, False, True, False, False], [110, 3, 2, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [9, 16, 192, 121, 141, 65, 125, 95, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [9, 16, 192, 121, 141, 65, 125, 95, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [2, 0, 180, 136, 106, 154, 108, 114, 0, 0, 0, 0, 0, 0, 180, 17, 110, 3, False, 116, 44, 44, 0, 108, 196, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1, 1.1, [120, 2, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [55, 14, 2, [1], 0, 0, 0, 3, False, False, True, False, False, False, False, False], [0, 2, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [0, 0, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False]]

r2 = [[2, 0, 180, 136, 106, 154, 108, 114, 0, 0, 0, 0, 0, 0, 180, 17, 110, 3, False, 116, 44, 44, 0, 108, 196, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1, 1.1, [120, 2, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [55, 14, 2, [1], 0, 0, 0, 3, False, False, True, False, False, False, False, False], [0, 2, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [9, 16, 192, 121, 141, 65, 125, 95, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [14, 16, 203, 201, 141, 72, 113, 71, 0, 0, 0, 0, 0, 0, 203, 18, 48, 9, False, 220, 220, 4, 0, 60, 4, 31, 31, 31, 31, 31, 31, 1, 1.1, 1, 0.9, 1, 1, [80, 16, 1, [1], 0, 0, 0, True, False, False, False, False, False, False, False], [60, 14, 1, [1], 0, 0, 0, True, False, False, False, False, False, False, False], [0, 7, 1, [1], 0, 0, 0, True, False, False, False, False, False, False, False], [70, 14, 1, [1], 0, 0, 1, True, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [9, 16, 192, 121, 141, 65, 125, 95, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [0, 0, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False]]

r3 = [[9, 16, 192, 121, 141, 65, 125, 95, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [7, 8, 191, 183, 151, 65, 73, 152, 0, 0, 0, 0, 0, 0, 191, 1, 176, 8, False, 4, 252, 0, 0, 0, 252, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1, 1.1, [120, 8, 1, [1], 0, 0, 0, True, True, False, False, False, False, False, False], [120, 7, 1, [1], 0, 0, 0, True, False, False, False, False, False, False, False], [100, 8, 1, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [3, 6, 131, 90, 134, 176, 81, 206, 0, 0, 0, 0, 0, 0, 131, 23, 181, 13, False, 0, 0, 0, 252, 4, 252, 31, 31, 31, 31, 31, 31, 1, 0.9, 1, 1, 1, 1.1, [70, 6, 2, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [55, 6, 2, [1], 0, 0, 0, 3, False, False, False, False, False, True, False, False], [110, 3, 2, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [2, 0, 180, 136, 106, 154, 108, 114, 0, 0, 0, 0, 0, 0, 180, 17, 110, 3, False, 116, 44, 44, 0, 108, 196, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1, 1.1, [120, 2, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [55, 14, 2, [1], 0, 0, 0, 3, False, False, True, False, False, False, False, False], [0, 2, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [0, 0, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False]]

r4 = [[7, 8, 191, 183, 151, 65, 73, 152, 0, 0, 0, 0, 0, 0, 191, 1, 176, 8, False, 4, 252, 0, 0, 0, 252, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1, 1.1, [120, 8, 1, [1], 0, 0, 0, True, True, False, False, False, False, False, False], [120, 7, 1, [1], 0, 0, 0, True, False, False, False, False, False, False, False], [100, 8, 1, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [9, 16, 192, 121, 141, 65, 125, 95, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [3, 6, 131, 90, 134, 176, 81, 206, 0, 0, 0, 0, 0, 0, 131, 23, 181, 13, False, 0, 0, 0, 252, 4, 252, 31, 31, 31, 31, 31, 31, 1, 0.9, 1, 1, 1, 1.1, [70, 6, 2, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [55, 6, 2, [1], 0, 0, 0, 3, False, False, False, False, False, True, False, False], [110, 3, 2, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [9, 16, 192, 121, 141, 65, 125, 95, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [0, 0, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False]]

r5 = [[2, 0, 180, 136, 106, 154, 108, 114, 0, 0, 0, 0, 0, 0, 180, 17, 110, 3, False, 116, 44, 44, 0, 108, 196, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1, 1.1, [120, 2, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [55, 14, 2, [1], 0, 0, 0, 3, False, False, True, False, False, False, False, False], [0, 2, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [9, 16, 192, 121, 141, 65, 125, 190, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 0, False, False, False], [9, 16, 192, 121, 141, 65, 125, 190, 0, 0, 0, 0, 0, 0, 192, 6, 136, 15, False, 148, 108, 124, 0, 68, 60, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1.1, 1, [120, 9, 1, [1], 0, 0.33, 0, True, False, False, False, False, False, False, False], [0, 7, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 9, 0, [1], 0, 0, 0, False, False, False, False, False, True, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 0, False, False, False], [7, 8, 191, 183, 151, 65, 73, 152, 0, 0, 0, 0, 0, 0, 191, 1, 176, 8, False, 4, 252, 0, 0, 0, 252, 31, 31, 31, 31, 31, 31, 1, 1, 1, 0.9, 1, 1.1, [120, 8, 1, [1], 0, 0, 0, True, True, False, False, False, False, False, False], [120, 7, 1, [1], 0, 0, 0, True, False, False, False, False, False, False, False], [100, 8, 1, [1], 0, 0, 0, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 4, False, False, False, False, False, False, False, False], [0, 1, 0, [1], 0, 0, 0, False, False, False, False, False, False, False, False], 1, False, False, False], [0, 0, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False], [False, 5, False, 5, False, 4, False, 5, False, False, False, False]]

# r1 = rework(r1)
# r2 = rework(r2)
# r3 = rework(r3)
# r4 = rework(r4)
# r5 = rework(r5)

# print(len(r1))
# print(len(r2))
# print(len(r3))
# print(len(r4))
# print(len(r5))

# print(r1,'\n\n')
# print(r2)

# An enviorment action is the action pair that the all 4 pokemon is going to take in a turn
# The action space on the other hand are all the possible action a pokemon can take during a turn including switch up
# For DQN, we are inputting state, and two human actions, and output two opponent actions, recall this is a stacklburg's game
# The last two element in an enviorment action are the actions outputed by the max damage AI function
# Comparing every posssible action from the action space with the max damage AI out put
# If they are the same, filter this action pair out, because this is a possible action pair the robot could take
# running these action though DQN, we choose the action pair that minimize the norm betweeen itself and the DQN output

# TODO create something to check the last two element in an action space with the max damage AI
def poosibleAction(ActionList,vec):
    # Initiate an empty possible action list
    PA = []
    # the actionlist is going to be a list that contains every possible move in a single turn
    # the vec is the last two elemtn in an enviorment action, aka the maxDamageAI action
    for idx in range(len(ActionList)):
        actionTemp = ActionList[idx]
        # The action Temp is going to be a list with four element, where each element is a list of the action for each pokemon
        if actionTemp[-2] == vec[0]:
            if actionTemp[-1] == vec[1]:
                PA.append(actionTemp)
    return PA

