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

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()
#for moves in database.movesDict.keys():
#	if(database.movesDict[moves].name == 'Head Smash'):
#		print(database.movesDict[moves])
annihilape = pokemon()
testMon = pokemon()
annihilape.addData(database)
testMon.addData(database)
field = field()
field.weather = 'Sun'
field.terrain = 'Grassy'
# print(annihilape.natureBoosts)
annihilape.addBoosts('at', +1)
# print(annihilape.stats)
testMove = database.movesDict['Flamethrower']
field.userSide = utils.checkInfiltrator(field.userSide)
# print(field.userSide.pokes[0].ignoresScreens)
annihilape = utils.checkSeedBoost(annihilape, field)
# print(annihilape.stats)
# print(utils.getBaseDamage(100, testMove.bp, annihilape.stats['at'], annihilape.stats['df']))
field.userSide.pokes[0] = annihilape
field.userSide.pokes[1] = testMon
field.opponentSide.pokes[0] = testMon
attacker = field.userSide.pokes[0]
attackerSide = 'user'
defender = field.opponentSide.pokes[0]
defenderSide = 'opponent'
move = attacker.moves[1]
testResult = result()
testResult = damageCalc.damageCalc(attacker, attackerSide, defender, defenderSide, move, field, testResult)
print(testResult.opponentDamage)
