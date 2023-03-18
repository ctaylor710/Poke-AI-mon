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
		speedMods.append(0.5)
	elif highestStat(pokemon) == 'sp' and ((pokemon.ability == 'Protosynthesis' and (field.weather == 'Sun' or pokemon.item == 'Booster Energy')) or \
		(pokemon.ability == 'Quark Drive' and (terrain == 'Electric' or pokemon.item == 'Booster Energy'))):
		speedMods.append(1.5)

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

def getMoveEffectiveness(move, defender, field):
	if field.isGhostRevealed and ('Ghost' in defender.name.types) and (move.type == 'Normal' or move.type == 'Fighting'):
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

def checkIntimidate(source, target):
	blocked = target.ability == 'Clear Body' or target.ability == 'White Smoke' or target.ability == 'Hyper Cutter' or target.ability == 'Full Metal Body' or \
		target.ability == 'Inner Focus' or target.ability == 'Own Tempo' or target.ability == 'Oblivious' or target.ability == 'Scrappy' or target.item == 'Clear Amulet'
	if source.ability == 'Intimidate' and ~blocked:
		if target.ability == 'Contrary' or target.ability == 'Defiant' or target.ability == 'Guard Dog':
			target.addBoosts('at', +1)
		elif target.ability == 'Simple':
			target.addBoosts('at', -2)
		else:
			target.addBoosts('at', -1)

		if target.ability == 'Competitive':
			target.addBoosts('sa', +2)
	return target


def checkInfiltrator(sourceSide):
	for pokemon in sourceSide:
		print(pokemon)
		if pokemon.ability == 'Infiltrator':
			pokemon.ignoresScreens = True
	return sourceSide

def checkSeedBoost(pokemon, field):
	if pokemon.item == 'None':
		return
	if field.terrain != 'None' and pokemon.item.find('Seed') != -1:
		terrainSeed = pokemon.item[:pokemon.item.find(' ')]
		if field.terrain == terrainSeed:
			if terrainSeed == 'Grassy' or terrainSeed == 'Electric':
				pokemon.addBoosts('df', -1) if pokemon.ability == 'Contrary' else pokemon.addBoosts('df', +1)
			else:
				pokemon.addBoosts('sd', -1) if pokemon.ability == 'Contrary' else pokemon.addBoosts('sd', +1)
	return pokemon


def chainMods(mods):
	M = 1
	for mod in mods:
		M *= mod
	return M

def getBaseDamage(level, basePower, userAtk, oppDef):
	return math.floor( math.floor( math.floor( (2*level)/5+2 )*basePower*userAtk/oppDef )/50+2 )

def highestStat(pokemon):
	bestStat = 'at'
	for stat in ['df', 'sa', 'sd', 'sp']:
		if getModifiedStat(pokemon.stats[stat], pokemon.boosts[stat]) > getModifiedStat(pokemon.stats[bestStat], pokemon.boosts[bestStat]):
			bestStat = stat
	return bestStat

def getFinalDamage(baseDamage, randInt, effectiveness, isBurned, stabMod, finalMod, protected):
	damage = math.floor(baseDamage*(85+randInt)/100) # Damage roll, damage is randomly between 85% and 100% of max possible damage
	damage = damage*stabMod
	damage = math.floor(damage*effectiveness)
	if isBurned:
		damage = math.floor(damage/2)
	if protected:
		damage = 0
	return math.round(max(0, damageAmount*finalMod))

def getWeightFactor(pokemon):
	if pokemon.ability == 'Heavy Metal':
		return 2
	elif pokemon.ability == 'Light Metal' or pokemon.item == 'Float Stone':
		return 0.5
	else:
		return 1

def handleFixedDamageMoves(pokemon, move):
	if move.name == 'Seismic Toss' or move.name == 'Night Shade':
		return pokemon.level
	elif move.name == 'Dragon Rage':
		return 40
	elif move.name == 'Sonic Boom':
		return 20
	else:
		return -1

