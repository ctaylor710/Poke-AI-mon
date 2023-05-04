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
from memory import MyMemory
from dqn import DQN

# TODO 1. Initialize the states
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

# botChoose is a function use the field and the index of the robot action to return the robot's moves and target
def botChoose(field, index):
    botMoveList, botTargetList = ActionSpaceBot(field.userSide.pokes[0], field.userSide.pokes[1], field.userSide.availablePokes, field)
    botMove = botMoveList[index]
    botTarget = botTargetList[index]
    return botMove, botTarget


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

# getHumanAction is a function that takes action vector as input and filter our the last two action, aka the human action
def getHumanAction(actionVector):
    HA = actionVector[-2] + actionVector[-1]
    return HA


# getHumanAction is a function that takes a field and output the human's action
def getHumanAction(field):
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
        action = env.actionVector(moveResult)
    return action

# TODO 2. Actual DQN stuff
# training parameters
batch_size = 128

# Creating environment
environment = env.CreateEnv()

# Creating agent
# For our DQN, we need to imput three things, sie of state, action and human action
# The length of the state is 518, the length of the actio is 636, the length of the human aaction is 318
state_size = 518
HA_size = 318
action_size = 636
agent = DQN(state_size, HA_size, action_size)

# Creating Memory
memory = MyMemory()
total_steps = 0

# Main loop
for i_episode in range(1, 100):
    episode_reward = 0
    done = False
    

    while not done:
        # Initialization
        state, pokes, avaliablePokes = field2SPA(myField)
        humanMove, humanTarget = ActionSpaceHuman (myField)
        
        # train the models
        if len(memory) > batch_size:
            loss = agent.update_parameters(memory, batch_size)
        
        # use policy to select action
        # choose random action for a while
        if total_steps < 1000:
            # choose two random moves and targets
            botMove, botTarget = botRandom(myField)

        else:
            # Recover what the moves and targets were from the robot action vector
            # TODO 1. Get Human's action
            # 1.1 get the human's move and human's target, both of them should be a vector with a size of two
            # humanMove, humanTarget = ActionSpaceHuman (myField)
            # 1.2 convert the moves and target into action, which we need to use the TakeMoves from damage calculation
            # TakeMove(attacker, attackerSide, defender, defenderSide, move, field, target, result)
            HA = getHumanAction(myField)
            # 2.1 get the index of the robot action by using the dqn funciton robotaction
            # But first make sure the state and human action we fed in are a single vector, which we can use the rework functino from singleVec.py
            stateOne = rework(state)
            HAOne = rework(HA)
            robotIndex = agent.robotaction(stateOne,HAOne)
            # 2.2 Use the index to recover the moves and target from the robot action space
            botMove, botTarget = botChoose(myField,robotIndex)
        
        # Organize all the moves and target up into two vectors
        moveVec = botMove + humanMove
        targetVec = botTarget + humanTarget
        # Append robot moves, targets to appropriate vectors        
        action, next_state, reward, dones, next_Field = env.Step(state, myField, pokes, moveVec, targetVec, avaliablePokes)
        # We also need next human action, which we can all the getHumanAction funtion
        HA = action[-2] + action[-1]
        next_HA = getHumanAction(next_Field)
        # TODO 1. push into memory
        # state, action, reward, next_state, next_action, done
        # 1.1 convert all state, action, and next_state
        stateOne = rework(state)
        actionOne = rework(action)
        next_state = rework(next_state)
        HA = rework(HA)
        next_HA = rework(next_HA)
        stateCombined = stateOne + HA
        next_stateCombined = next_state + next_HA
        # 1.2 pushing
        memory.push(stateCombined, actionOne, reward, next_stateCombined, done)
        # 1.3 updating
        episode_reward += reward
        myField = next_Field
        total_steps += 1
    
    print("Episode: {}, Reward: {}".format(i_episode, round(episode_reward, 2)))




        

