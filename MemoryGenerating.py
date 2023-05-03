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

# Creating states
state = env.StateVector(myField, myField.userSide.pokes, myField.opponentSide.pokes)
pokes = myField.userSide.pokes + myField.opponentSide.pokes
botmoveList, bottargetList = ActionSpaceBot(myField.userSide.pokes[0], myField.userSide.pokes[1], myField.userSide.availablePokes, myField)
# randomly pick a bot moves
print(len(botmoveList))
print(len(bottargetList))
index = random.randint(0, 195)  # recall the length of the move List is 196
botmove = botmoveList[index]
bottarget = bottargetList[index]
humanmove, humantarget  = ActionSpaceHuman(myField)
moves = botmove + humanmove
targets = bottarget + humantarget
availablePokes = myField.userSide.availablePokes

print(targets)
action, next_state, reward, dones = env.Step(state, myField, pokes, moves, targets, availablePokes)

print('action:',action,'\n\nNext State',next_state,'\n\nReward',reward,'\n\nDone',dones)

stateOne = rework(state)
actionOne = rework(action)
print(len(stateOne))
print(len(actionOne))