from database.database import database
from database.moves import move
from database.pokeTypes import pokeType
from database.species import species
from database.natures import nature
from pokemon import pokemon
from field import field
from side import side
import utils

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()
#for types in database.typesDict.keys():
#	print(types)
annihilape = pokemon()
annihilape.addData(database)
print(annihilape)
field = field()
field.weather = 'Sun'
print(annihilape.stats)
annihilape.addBoosts('at', +1)
annihilape.stats = utils.computeFinalStats(annihilape, field, 'user')
print(annihilape.stats)
testMove = database.movesDict['Population Bomb']
print(utils.getMoveEffectiveness(testMove, annihilape, False, field))
print(utils.isGrounded(annihilape, field))
