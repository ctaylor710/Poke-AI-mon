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
import RL
import torch

endLoop = False; localFilePath = None; targetFilePath = None; optimizerFilePath = None; memoryFilePath = None
while not endLoop:
	qnetwork_local, localFilePath, qnetwork_target, targetFilePath, optimizer, optimizerFilePath, memory, memoryFilePath = RL.RLTraining(localFilePath, targetFilePath, optimizerFilePath, memoryFilePath)
	torch.save(qnetwork_local, localFilePath)
	torch.save(qnetwork_target, targetFilePath)
	torch.save(optimizer, optimizerFilePath)
	with open('memory.pkl', 'wb') as handle:
		pickle.dump(memory, handle, protocol=pickle.HIGHEST_PROTOCOL)
	string = input('Type \'end\' to finish training. Otherwise, press any key to continue: ')
	if string == 'end':
		endLoop = True

