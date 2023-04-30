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
file = open('DemonstrationData.txt', 'a')
for i in range(2):
	states, actions = env.demonstration()
	for j in range(len(states)-1):
		file.write(str(states[j]))
		file.write('\n\n')
		file.write(str(actions[j]))
		file.write('\n\n')

file.close()