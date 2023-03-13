import math
from database.database import database

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()

def isGrounded(pokemon, field):
	return field.gravity or pokemon.item == 'Iron Ball' or \
	(~('Flying' in pokemon.name.types) and pokemon.ability != 'Levitate'and pokemon.item != 'Air Balloon')

def getModifiedStat(stat, number):
	num = 0
	denom = 1
	modernGenBoostTable = [[2, 8], [2, 7], [2, 6], [2, 5], [2, 4], [2, 3], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], [8, 2]]
	stat = stat*modernGenBoostTable[6+number][num]
	stat = math.floor(stat/modernGenBoostTable[6+number][denom])
	return stat

def getFinalSpeed(pokemon, field, sideName):
	weather = field.weather
	terrain = field.terrain
	speed = getModifiedStat(pokemon.stats['sp'], pokemon.boosts['sp'])
	speedMods = []
	side = field.userSide
	if sideName == 'opponent':
		side = field.opponentSide

	if side.tailwind:
		speedMods.append(2)
	if (pokemon.ability == 'Unburden' and pokemon.item == 'None') or \
		(pokemon.ability == 'Chlorophyll' and field.weather == 'Sun') or \
		(pokemon.ability == 'Sand Rush' and field.weather == 'Sand') or \
		(pokemon.ability == 'Swift Swim' and field.weather == 'Rain') or \
		(pokemon.ability == 'Slush Rush' and field.weather == 'Snow') or \
		(pokemon.ability == 'Surge Surfer' and field.terrain == 'Electric'):
		speedMods.append(2)
	elif pokemon.ability == 'Quick Feet' and pokemon.status != 'Healthy':
		speedMods.append(1.5)
	elif pokemon.ability == 'Slow Start' and pokemon.abilityOn:
		speedModes.append(0.5)

	if pokemon.item == 'Choice Scarf':
		speedMods.append(1.5)
	elif pokemon.item == 'Iron Ball':
		speedMods.append(0.5)
	elif pokemon.item == 'Quick Powder' and pokemon.name == 'Ditto':
		speedMods.append(2)

	for mods in speedMods:
		speed = speed * mods
	speed = round(speed)

	if pokemon.status == 'Paralyze' and pokemon.ability != 'Quick Feet':
		speed = math.floor(speed/2)
	speed = min(10000, speed)

	return max(0, speed)

def computeFinalStats(pokemon, field, sideName):
	for stat in pokemon.name.bs.keys():
		if stat == 'sp':
			pokemon.stats['sp'] = getFinalSpeed(pokemon, field, sideName)
		else:
			pokemon.stats[stat] = getModifiedStat(pokemon.stats[stat], pokemon.boosts[stat])
	return pokemon.stats

def effectiveness(attackingType, defendingTypes):
	effectiveness = 1
	for types in defendingTypes:
		effectiveness *= database.typesDict[attackingType].effectiveness[types]
	return effectiveness

def getMoveEffectiveness(move, defender, isGhostRevealed, field):
	if isGhostRevealed and ('Ghost' in defender.name.types) and (move.type == 'Normal' or move.type == 'Fighting'):
		return 1
	elif move.name == 'Freeze-Dry' and ('Water' in defender.name.types):
		return 2
	elif field.gravity and ('Flying' in defender.name.types) and move.type == 'Ground':
		otherType = defender.name.types[1] if defender.name.types[0] == 'Flying' else defender.name.types[0]
		return database.typesDict[move.type][otherType]
	elif move.name == 'Flying Press':
		return effectiveness('Fighting', defender.name.types) * effectiveness('Flying', defender.name.types)
	else:
		return effectiveness(move.type, defender.name.types)



