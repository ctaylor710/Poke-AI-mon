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
#for moves in database.speciesDict.keys():
#	if moves == 'Flutter Mane':
#		print(database.speciesDict[moves])
testTeam = []
fileName = input('Enter team sheet: ')
file = open(f'pokemonFiles/{fileName}')
index = -1
for line in file:
	line = line.strip()
	if len(line) > 0:
		words = line.split('@')
		words[0] = words[0].strip()
		if words[0] in database.speciesDict.keys():
			testTeam.append(pokemon())
			index += 1
	testTeam[-1].addDataLine(database, line)
print(testTeam[0], testTeam[1])

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
field.opponentSide.pokes[1] = annihilape
attacker = field.userSide.pokes[0]
attackerSide = 'user'
defender = field.opponentSide.pokes[0]
defenderSide = 'opponent'
move = attacker.moves[1]
testResult = result()
testResult = damageCalc.damageCalc(attacker, attackerSide, defender, defenderSide, move, field, 'opponent', testResult)
print(testResult.opponentDamage)
