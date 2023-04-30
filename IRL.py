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

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()

file = open("DemonstrationData.txt", "r")