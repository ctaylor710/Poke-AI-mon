"""
DQN Example
pip install gymnasium
pip install gymnasium[classic-control]

"""

import numpy as np
import torch
from torch.optim import Adam
from memory import MyMemory
from dqn import DQN
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
        move, target = env.maxDamageAI(field.opposingSide.pokes[i], field.opposingSide.pokes[-1*i + 1], field.userSide, field)
        moveResult = result()
        for t in target:
            moveResult = damageCalc.TakeMove(field.opposingSide.pokes[i], 'opponent', field.userSide.pokes[i], 'user', move, field, t, moveResult)
            action = env.actionVector(moveResult)
        # reward = env.RewardModel(state, action, theta)
        actionVec.append(action)
        # rewardVec.append(reward)
    # index = np.argmax(rewardVec)
    # HA =  actionVec[index]
    return(actionVec)


    


# training parameters
batch_size = 128

# Environment


# Agent
# input state and action sizes of our environment
HA_size = 310
agent = DQN(, )

# Memory
memory = MyMemory()
total_steps = 0

# Main loop
for i_episode in range(1, 10001):

    episode_reward = 0
    done = False
    truncated = False
    state, _ = env.reset()

    while not done and not truncated:

        # train the models
        if len(memory) > batch_size:
            loss = agent.update_parameters(memory, batch_size)

        # use policy to select action
        # choose random action for a while
        if total_steps < 1000:
            action = env.action_space.sample()
        # then use the learned policy
        else:
            action = agent.select_action(state, 0.01)

        # transition to next_state and store data
        next_state, reward, done, truncated, _ = env.step(action)
        episode_reward += reward
        memory.push(state, action, reward, next_state, done)
        state = next_state
        total_steps += 1

    print("Episode: {}, Reward: {}".format(i_episode, round(episode_reward, 2)))
