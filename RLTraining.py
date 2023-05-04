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

endLoop = False; localFilePath = None; targetFilePath = None
while not endLoop:
	qnetwork_local, localFilePath, qnetwork_target, targetFilePath = RL.RLTraining(localFilePath, targetFilePath)
	torch.save(qnetwork_local, localFilePath)
	torch.save(qnetwork_target, targetFilePath)
	string = input('Type \'end\' to finish training. Otherwise, press any key to continue: ')
	if string == 'end':
		endLoop = True

