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
import pickle
from singleVec import * 
from actionSpace import *

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


# field2SPA is a function that use the fied as input and ouput the state, pokemon and avaliable pokemons
def field2SPA(field):
    state = env.StateVector(field, field.userSide.pokes, field.opponentSide.pokes)
    pokes = field.userSide.pokes + field.opponentSide.pokes
    avaliablePokes = field.userSide.availablePokes
    return state, pokes, avaliablePokes

# botRandom is a function that takes field as input and output two random pokmon moves and their target
def botRandom(field):
    botMoveList, botTargetList = ActionSpaceBot(field.userSide.pokes[0], field.userSide.pokes[1], field.userSide.availablePokes, field)
    # randomly pick a bot moves
    index = random.randint(0, 193)  # recall the length of the move List is 194
    botMove = botMoveList[index]
    botTarget = botTargetList[index]
    return botMove, botTarget


# getHumanAction is a function that takes a field and output the human's action
def getHumanAction(field):
    action = []
    humanMove, humanTarget = ActionSpaceHuman (field)
    for idx in range(2):
        attacker  = field.opponentSide.pokes[idx]
        attackerSide = 'opponent'
        movetemp = humanMove[idx]
        target = humanTarget[idx]
        moveResult = result()
        for t in target:
            if t <= 2:
                defender = field.userSide.pokes[t-1]
                defenderSide = 'user'
            else:
                defender = field.opponentSide.pokes[t-3]
                defenderSide = 'opponent'

            moveResult = damageCalc.TakeMove(attacker, attackerSide, defender, defenderSide, movetemp, field, t, moveResult)
        action += env.actionVector(moveResult)
    return action


a = getHumanAction(myField)
print(len(rework(a)))


def reMovesNTarget(action):
    newMoveVec = []
    newTargetVec = [[],[],[],[]]
    for a in action:
        pokeMove = a[-1]
        target = a[1]
        user = a[0]
        newMoveVec.append(pokes[user].moves[pokeMove])
        newTargetVec[user].append(target)
    return newMoveVec, newTargetVec






# TODO 1. Creating four moves and target
# 1.1 create bot moves and target
botMove, botTarget = botRandom(myField)
# 1.2 create human moves and target, which we need user pokemon, ally pokemon, opposingSide and field
humanMove, humanTarget = ActionSpaceHuman (myField)
print(humanMove)
print(humanTarget)

a = getHumanAction(myField)
print(a)
# a = humanTarget[0][0]
# print(humanMove)

# for idx in range(2):
#     attacker  = myField.opponentSide.pokes[idx]
#     attackerSide = 'opponent'
#     movetemp = humanMove[idx]
#     target = humanTarget[idx]
#     moveResult = result()
#     for t in target:
#         if t <= 2:
#             defender = myField.userSide.pokes[t-1]
#             defenderSide = 'user'
#         else:
#             defender = myField.opponentSide.pokes[t-3]
#             defenderSide = 'opponent'

#         moveResult = damageCalc.TakeMove(attacker, attackerSide, defender, defenderSide, movetemp, myField, t, moveResult)
#     action = env.actionVector(moveResult)
# print(action)




# # 1.3 combine them together to create the actual moves and target vector
# moveVec = botMove + humanMove
# targetVec = botTarget + humanTarget
# # TODO 2. Create actions
# state, pokes, avaliablePokes = field2SPA(myField)
# action, next_state, reward, dones, next_field = env.Step(state, myField, pokes, moveVec, targetVec, avaliablePokes)
# # print(action)
# # TODO 3. Recover target from action
# # print('old moves')
# # [print(moveVec[i].name) for i in range(4)]
# # print('old targets', targetVec)
# # for i in range(4):
# #     print('available moves')
# #     [print(pokes[action[i][0]].moves[j].name) for j in range(4)]
# #     if moveVec[i] != 'switch':
# #         print('user', action[i][0])
# #         print('move taken', moveVec[action[i][0]].name)
# #     else:
# #         print('move taken', moveVec[i])
# # # The target are the second element in a pokemon's action
# # for a in action:
# #     targetRaw = a[1]
# #     print('target', targetRaw)
# #     moveIndices = a[-1]
# #     print('move index', moveIndices)




# print('new moves')
# [print(moveVec[i].name) for i in range(4)]
# print('new targets', newTargetVec)

    


# print(botMove, botTarget)
# print(humanMove,humanTarget)




# # Generating data for the current state
# state, pokes, moves, targets, avaliablePokes = field2SPMTA(myField)
# action, next_state, reward, dones, next_field = env.Step(state, myField, pokes, moves, targets, avaliablePokes)
# # We also need the next action for our DQN, we can get the next action by calling the step function one more time
# # To call the Step function we need new moves and targets, which we can get from our next_field
# next_state, next_pokes, next_moves, next_targets, next_avaliablePokes = field2SPMTA(next_field)
# next_action,_,_,_,_ = env.Step(next_state, next_field, next_pokes, next_moves, next_targets, next_avaliablePokes)
# print(next_action,'\n\n')
# HA = getHumanAction(next_action)
# print(HA)
# # print(next_action)

# stateOne = rework(state)
# actionOne = rework(action)
# HA = rework(HA)
# print(len(HA))
# print(len(stateOne))
# print(len(actionOne))

# state = env.StateVector(myField, myField.userSide.pokes, myField.opponentSide.pokes)
# pokes = myField.userSide.pokes + myField.opponentSide.pokes
# availablePokes = myField.userSide.availablePokes
# botmoveList, bottargetList = ActionSpaceBot(myField.userSide.pokes[0], myField.userSide.pokes[1], myField.userSide.availablePokes, myField)
# # randomly pick a bot moves
# # print(len(botmoveList))
# # print(len(bottargetList))
# index = random.randint(0, 193)  # recall the length of the move List is 194
# botmove = botmoveList[index]
# bottarget = bottargetList[index]
# humanmove, humantarget  = ActionSpaceHuman(myField)
# moves = botmove + humanmove


# # print(moves[0].name,moves[1].name,moves[2].name,moves[3].name)
# targets = bottarget + humantarget

# print(pokes)

# So the things we need in a memory are state, action, next state, next action, reward, and done
# we already have the state and we can use the step function to get the action, nextstate, rewarad and done


# # We can call the step function for a second time to get the next action
# # But first we need to recover the moves and targets from the action
# # Notice that the action has four element [p1,p2,p3,p4] from the frou pokemon on the field
# # The second element in the individule pokemon action is the target like [1,-1,-1]. the [-1] there is to keep the target same size

# next_target = []
# indexList = []
# for a in action:
#     target_temp = a[1]
#     target = []
#     for element in target_temp:
#         if element != -1:
#             target.append(element)
#     next_target.append(target)
# # print(indexList)

# # The next thing we need is the next move, we can get the Human'smove by calling the max damage AI and bot's move by picking random move






# # print('action:',action)#,'\n\nNext State',next_state,'\n\nReward',reward,'\n\nDone',dones)

