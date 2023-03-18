from database.database import database
from database.moves import move
from database.pokeTypes import pokeType
from database.species import species
from database.natures import nature
from pokemon import pokemon
from field import field
from side import side
import utils
import damageCalc

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()
#for types in database.typesDict.keys():
#	print(types)
annihilape = pokemon()
testMon = pokemon()
annihilape.addData(database)
testMon.addData(database)
print(annihilape)
field = field()
field.weather = 'Sun'
field.terrain = 'Grassy'
field.userSide.pokes[0] = annihilape
print(annihilape.stats)
annihilape.addBoosts('at', +1)
annihilape.stats = utils.computeFinalStats(annihilape, field, 'user')
print(annihilape.stats)
testMove = database.movesDict['Flamethrower']
annihilape = utils.checkInfiltrator([annihilape])[0]
print(annihilape.ignoresScreens)
annihilape = utils.checkSeedBoost(annihilape, field)
print(annihilape.boosts)
print(utils.getBaseDamage(100, testMove.bp, annihilape.stats['at'], annihilape.stats['df']))
