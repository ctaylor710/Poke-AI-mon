"""
-This script calculates the damage dealt by a move between an attacker and defender.
-Much of this code is adapted from this repository: https://github.com/smogon/damage-calc/tree/master/
 *This repository is a reputable resource in the Pokemon community that provides accurate battle data that can
  be used for damage calculations under any battle state.
-These calculations assume full knowledge of the battle state, i.e., the full state of the opposing pokemon must
be passed in. In reality this will not be known, and the robot will have to make decisions on what to assume each
of the unknown state values are.

"""
from database.database import database
from pokemon import pokemon
import utils

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()

def damageCalc(attacker, attackerSide, defender, defenderSide, move, field):

	print(attacker.boosts)
	print(defender.boosts)
	attacker = utils.checkSeedBoost(attacker, field)
	defender = utils.checkSeedBoost(defender, field)
	attacker = utils.checkIntimidate(defender, attacker)
	defender = utils.checkIntimidate(attacker, defender)

	attacker.stats = utils.computeFinalStats(attacker, field, attackerSide)
	defender.stats = utils.computeFinalStats(defender, field, defenderSide)

	if attackerSide == 'user':
		attackerSide = field.userSide
		defenderSide = field.opponentSide
	else:
		attackerSide = field.opponentSide
		defenderSide = field.userSide

	attackerSide = utils.checkInfiltrator(attackerSide)
	defenderSide = utils.checkInfiltrator(defenderSide)

	result = [0, 0] # [Damage dealt to opponent, damage dealt to self]
	print(attacker.boosts)
	print(defender.boosts)

	if move.category == 'Status' and move.name != 'Nature Power':
		return result

	if defenderSide.isProtected and ~move.breaksProtect:
		return result

	defenderIgnoresAbility = defender.ability == 'Full Metal Body' or defender.ability == 'Neutralizing Gas'
	attackerIgnoresAbility = attacker.ability == 'Mold Breaker'

	isCritical = ~(defender.ability == 'Battle Armor' or defender.ability == 'Shell Armor') and \
		(move.isCrit or (attacker.ability == 'Merciless' and (defender.status == 'Posion' or defender.status == 'Toxic')))

	moveType = move.type
	if move.name == 'Nature Power' or move.name == 'Terrain Pulse':
		if field.terrain == 'Electric':
			moveType = 'Electric'
		elif field.terrain == 'Grassy':
			moveType = 'Grass'
		elif field.terrain == 'Misty':
			moveType = 'Fairy'
		elif field.terrain == 'Psychic':
			moveType = 'Psychic'
		else:
			moveType = 'Normal'
	elif move.name == 'Revelation Dance':
		moveType = attacker.name.types[0]
	elif move.name == 'Raging Bull':
		if attacker.name.name == 'Tauros-Paldea-Combat':
			moveType = 'Fighting'
		elif attacker.name.name == 'Tauros-Paldea-Blaze':
			moveType = 'Fire'
		elif attacker.name.name == 'Tauros-Paldea-Aqua':
			moveType = 'Water'


	hasAteAbilityTypeChange = False
	isPixilate = False

	noTypeChange = move.name == 'Revelation Dance' or move.name == 'Nature Power' or move.name == 'Terrain Pulse' or \
		(move.name == 'Tera Blast' and attacker.isTera)

	if ~noTypeChange:
		normal = move.type == 'Normal'
		isPixilate = attacker.ability == 'Pixilate'
		if isPixilate and normal:
			moveType = 'Fairy'

		if isPixilate:
			hasAteAbilityTypeChange = True

	if move.name == 'Tera Blast' and attacker.isTera:
		moveType = attacker.tera

	move.type = moveType

	if (attacker.ability == 'Triage' and move.drain > 0) or \
		(attacker.ability == 'Gale Wings' and move.type == 'Flying' and attacker.currHP == attacker.stats['hp']):
		move.priority = 1

	isGhostRevealed = attacker.ability == 'Scrappy' or defenderSide.isForesight

	typeEffectiveness = utils.getMoveEffectiveness(move, defender, field)

	if defender.isTera:
		storage = defender.name.types.copy()
		defender.name.types = [defender.tera]
		typeEffectiveness = utils.getMoveEffectiveness(move, defender, field)
		defender.name.types = storage

	if typeEffectiveness == 0 and move.type == 'Ground' and defender.item == 'Iron Ball' and defender.ability != 'Klutz':
		typeEffectiveness = 1

	if typeEffectiveness == 0:
		return result

	if (defender.ability == 'Wonder Guard' and typeEffectiveness <= 1) or \
		(move.type == 'Grass' and defender.ability == 'Sap sipper') or \
		(move.type == 'Fire' and (defender.ability == 'Flash Fire' or defender.ability == 'Well-Baked Body')) or \
		(move.type == 'Water' and (defender.ability == 'Dry skin' or defender.ability == 'Storm Drain' or defender.ability == 'Water Absorb')) or \
		(move.type == 'Electric' and (defender.ability == 'Lightning Rod' or defender.ability == 'Motor Drive' or defender.ability == 'Volt Absorb')) or \
		(move.type == 'Ground' and ~field.isGravity and defender.item != 'Iron Ball' and defender.ability == 'Levitate') or \
		(move.isBullet and defender.ability == 'Bulletproof') or \
		(move.isSound and defender.ability == 'Soundproof') or \
		(move.priority > 0 and (defender.ability == 'Dazzling' or defender.ability == 'Armor Tail')) or \
		(move.type == 'Ground' and defender.ability == 'Earth Eater') or \
		(move.isWind and defender.ability == 'Wind Rider'):
		return result

	if move.type == 'Ground' and ~field.isGravity and defender.item == 'Air Balloon':
		return result

	if move.priority > 0 and field.terrain == 'Psychic' and utils.isGrounded(defender, field):
		return result

	weightBasedMove = move.name == 'Heat Crash' or move.name == 'Heavy Slam' or move.name == 'Low Kick' or move.name == 'Grass Knot'

	fixedDamage = utils.handleFixedDamageMoves(attacker, move)
	if fixedDamage > 0:
		return [fixedDamage, 0]

	if move.name == 'Final Gambit':
		result = [attacker.currHP, attacker.currHP]
		return result

	basePower = calculateBasePower(attacker, attackerSide, defender, defenderSide, move, field, hasAteAbilityTypeChange)

	if move.bp == 0:
		return result

	attack = calculateAttack(attacker, attackerSide, defender, defenderSide, move, field, isCritical)
	attackSource = defender if move.name == 'Foul Play' else attacker
	if move.name == 'Tera Blast' and attackSource.isTera:
		move.category = 'Physical' if attackSource.stats['at'] > attackSource.stats['sa'] else 'Special'
	attackStat = 'df' if move.name == 'Body Press' else ('sa' if move.category == 'Special' else 'at')

	defense = calculateDefense(attacker, attackerSide, defender, defenderSide, move, field, isCritical)
	hitsPhysical = move.overrideDefensiveStat == 'def' or move.category == 'Physical'
	defenseStat = 'df' if hitsPhysical else 'sd'

	baseDamage = utils.getBaseDamage(attacker.level, basePower, attack, defense)

	isSpread = move.target == 'allAdjacent' or move.target == 'allAdjacentFoes'
	if isSpread:
		baseDamage *= 0.75

	noWeatherBoost = defender.item == 'Utility Umbrella'
	if ~noWeatherBoost and (field.weather == 'Sun' and move.type == 'Fire') or \
		(field.weather == 'Rain' and move.type == 'Water'):
		baseDamage *= 1.5
	elif ~noWeatherBoost and (field.weather == 'Sun' and move.type == 'Water') or \
		(field.weather == 'Rain' and move.type == 'Fire'):
		baseDamage *= 0.5

	if isCritical:
		baseDamage *= 1.5

	stabMod = 1
	if move.type in attacker.name.types:
		stabMod += 0.5
	elif (attacker.ability == 'Protean' or attacker.ability == 'Libero') and ~attacker.isTera:
		stabMod += 0.5

	teraType = attacker.tera
	if teraType == move.type:
		stabMod += 0.5

	if attacker.ability == 'Adaptability' and stabMod > 1:
		stabMod += (0.25 if pokemon.isTera and (teraType in attacker.name.types) else 0.5)

	applyBurn = attacker.status == 'Burn' and move.category == 'Physical' and ~attacker.ability == 'Guts' and ~move.name == 'Facade'

	finalMods = calculateFinalMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, typeEffectiveness)

	protect = False
	if defenderSide.isProtected:
		protect = True

	finalMod = utils.chainMods(finalMods)

	damage = []
	for i in range(16):
		damage.append(utils.getFinalDamage(baseDamage, i, typeEffectiveness, applyBurn, stabMod, finalMod, protect))

	result = damage

	return result

def calculateBasePower(attacker, attackerSide, defender, defenderSide, move, field, hasAteAbilityTypeChange):
	turnOrder = 'first' if attacker.stats['sp'] > defender.stats['sp'] else 'last'

	basePower = 0

	if move.name == 'Payback':
		basePower = move.bp * (2 if turnOrder == 'last' else 1)
	elif move.name == 'Pursuit':
		switching = defenderSIde.isSwitching == 'out'
		basePower = move.bp * (2 if switching else 1)
	elif move.name == 'Electro Ball':
		r = math.floor(attacker.stats['sp']/defender.stats['sp'])
		if defender.stats['sp'] == 0:
			basePower = 40
		else:
			basePower = 150 if r >= 4 else (120 if r >= 3 else (80 if r >= 2 else( 60 if r >= 1 else 40)))
	elif move.name == 'Gyro Ball':
		if attacker.stats['sp'] == 0:
			basePower = 1
		else:
			basePower = min(150, math.floor(25*defender.stats['sp']/attacker.stats['sp']) + 1)
	elif move.name == 'Punishment':
		basePower = min(200, 60 + 20*utils.countBoosts(defender.boosts))
	elif move.name == 'Low Kick' or move.name == 'Grass Knot':
		w = defender.weightkg * utils.getWeightFactor(defender)
		basePower = 120 if w >= 200 else (100 if w >= 100 else (80 if w >= 50 else (60 if w >= 25 else (40 if w >= 10 else 20))))
	elif move.name == 'Hex' or move.name == 'Infernal Parade':
		basePower = move.bp * (2 if defender.status != 'Healthy' or defender.ability == 'Comatose' else 1)
	elif move.name == 'Heavy Slam' or move.name == 'Heat Crash':
		wr = (attacker.weightkg * utils.getWeightFactor(attacker)) / (defender.weightkg * utils.getWeightFactor(defender))
		basePower = 120 if wr >= 5 else (100 if wr >= 4 else (80 if wr >= 3 else (60 if wr >= 2 else 40)))
	elif move.name == 'Stored Power' or move.name == 'Power Trip':
		basePower = 20 + 20*utils.countBoosts(attacker.boosts)
	elif move.name == 'Acrobatics':
		basePower = move.bp * (2 if attacker.item == 'Flying Gem' or attacker.item == 'None' else 1)
	elif move.name == 'Wake-Up Slap':
		basePower = move.bp * (2 if defender.status == 'Sleep' or defender.ability == 'Comatose' else 1)
	elif move.name == 'Terrain Pulse':
		basePower = move.bp * (2 if utils.isGrounded(attacker, field) and field.terrain != 'None' else 1)
	elif move.name == 'Eruption' or move.name == 'Water Spout':
		basePower = max(1, math.floor(150*attacker.currHP/attacker.stats['hp']))
	elif move.name == 'Flail' or move.name == 'Reversal':
		p = math.floor(48*attacker.currHP/attacker.stats['hp'])
		basePower = 200 if p <= 1 else (150 if p <= 4 else (100 if p <= 9 else (80 if p <= 16 else (40 if p <= 32 else 20))))
	elif move.name == 'Triple Axel':
		basePower = 40 if move.hits == 3 else (30 if move.hits == 2 else 20)
	elif move.name == 'Triple Kick':
		basePower = 30 if move.hits == 3 else (15 if move.hits == 2 else 10)
	else:
		basePower = move.bp

	if basePower == 0:
		return 0

	bpMods = calculateBPMods(attacker, attackerSide, defender, defenderSide, move, field, basePower, hasAteAbilityTypeChange, turnOrder)
	basePower = max(1, basePower*utils.chainMods(bpMods))

	return basePower

def calculateBPMods(attacker, attackerSide, defender, defenderSide, move, field, basePower, hasAteAbilityTypeChange, turnOrder):
	bpMods = []

	resistedKnockOffDamage = defender.item == 'None'

	if (move.name == 'Facade' and (attacker.status=='Burn' or attacker.status=='Paralyze' or attacker.status=='Poison' or attacker.status=='Toxic')) or \
		(move.name == 'Brine' and defender.currHP <= defender.stats['hp']/2) or \
		(move.name == 'Venoshock' and (defender.status == 'Posion' or defender.status == 'Toxic')):
		bpMods.append(2)
	elif move.name == 'Expanding Force' and utils.isGrounded(attacker, field) and field.terrain == 'Psychic':
		move.target = 'allAdjacentFoes'
		bpMods.append(1.5)
	elif (move.name == 'Knock Off' and ~resistedKnockOffDamage) or \
		(move.name == 'Grav Apple' and field.isGravity):
		bpMods.append(1.5)
	elif (move.name == 'Solar Beam' or move.name == 'Solar Blade') and \
		(field.weather == 'Rain' or field.weather == 'Sand' or field.weather == 'Snow'):
		bpMods.append(0.5)
	elif move.name == 'Collision Course' or move.name == 'Electro Drift':
		isGhostRevealed = attacker.ability == 'Scrappy' or defenderSide.isForesight
		effectiveness = utils.getMoveEffectiveness(move, defender, field)
		if effectiveness >= 2:
			bpMods.append(4/3)

	if attackerSide.isHelpingHand:
		bpMods.append(1.5)

	terrainMultiplier = 1.3
	if utils.isGrounded(attacker, field):
		if (field.terrain == 'Electric' and move.type == 'Electric') or \
			(field.terrain == 'Grassy' and move.type == 'Grass') or \
			(field.terrain == 'Psychic' and move.type == 'Psychic'):
			bpMods.append(terrainMultiplier)
	if utils.isGrounded(defender, field):
		if (field.terrain == 'Misty' and move.type == 'Dragon') or \
			(field.terrain == 'Grassy' and (move.name == 'Bulldoze' or move.name == 'Earthquake')):
			bpMods.append(0.5)

	if (attacker.ability == 'Technician' and basePower <= 60) or \
		(attacker.ability == 'Flare Boost' and attacker.status == 'Burn' and move.category == 'Special') or \
		(attacker.ability == 'Toxic Boost' and (attacker.status == 'Poison' or attacker.status == 'Toxic') and move.category == 'Physical') or \
		(attacker.ability == 'Mega Launcher' and move.isPulse) or \
		(attacker.ability == 'Strong Jaw' and move.isBite) or \
		(attacker.ability == 'Steely Spirit' and move.type == 'Steel') or \
		(attacker.ability == 'Sharpness' and move.isSlicing):
		bpMods.append(1.5)

	if(attacker.ability == 'Sheer Force' and (move.secondaries or (move.name == 'Jet Punch' or move.name == 'Order Up'))) or \
		(attacker.ability == 'Sand Force' and field.weather == 'Sand' and (move.type == 'Rock' or move.type == 'Ground' or move.type == 'Steel')) or \
		(attacker.ability == 'Analytic' and (turnOrder != 'first' or defenderSide.isSwitching == 'out')) or \
		(attacker.ability == 'Tough Claws' and move.makesContact) or \
		(attacker.ability == 'Punk Rock' and move.isSound):
		bpMods.append(1.3)

	if attacker.ability == 'Rivalry' and attacker.gender != 'N' and defender.gender != 'N':
		if attacker.gender == defender.gender:
			bpMods.append(1.25)
		else:
			bpMods.append(0.75)

	if hasAteAbilityTypeChange:
		bpMods.append(1.2)

	if (attacker.ability == 'Reckless' and (move.recoil > 0 or move.hasCrashDamage)) or \
		(attacker.ability == 'Iron Fist' and move.isPunch):
		bpMods.append(1.2)

	if attacker.item == 'Punching Glove' and move.isPunch:
		bpMods.append(1.1)

	if defender.ability == 'Heatproof' and move.type == 'Fire':
		bpMods.append(0.5)
	elif defender.ability == 'Dry Skin' and move.type == 'Fire':
		bpMods.append(1.25)

	if attacker.ability == 'Supreme Overlord' and attacker.alliesFainted > 0:
		powMod = [1, 1.1, 1.2, 1.3, 1.4, 1.5]
		bpMods.append(powMod[min(5, attacker.alliesFainted)])

	if (attacker.item == 'Muscle Band' and move.category == 'Physical') or \
		(attacker.item == 'Wise Glasses' and move.category == 'Special'):
		bpMods.append(1.1)

	return bpMods

def calculateAttack(attacker, attackerSide, defender, defenderSide, move, field, isCritical):
	attackSource = defender if move.name == 'Foul Play' else attacker
	if move.name == 'Tera Blast' and attackSource.isTera:
		move.category = 'Physical' if attackSource.stats['at'] > attackSource.stats['sa'] else 'Special'
	attackStat = 'df' if move.name == 'Body Press' else ('sa' if move.category == 'Special' else 'at')

	if attackSource.boosts[attackStat] == 0 or (isCritical and attackSource.boosts[attackStat] < 0):
		attack = attackSource.rawStats[attackStat]
	elif defender.ability == 'Unaware':
		attack = attackSource.rawStats[attackStat]
	else:
		attack = attackSource.stats[attackStat]

	if attacker.ability == 'Hustle' and move.category == 'Physical':
		attack = round(attack*1.5)

	atMods = calculateAtMods(attacker, attackerSide, defender, defenderSide, move, field)
	attack = round(attack*utils.chainMods(atMods))

	return attack

def calculateAtMods(attacker, attackerSide, defender, defenderSide, move, field):
	atMods = []

	if (attacker.ability == 'Solar Power' and field.weather == 'Sun' and move.category == 'Special'):
		atMods.append(1.5)
	elif (attacker.ability == 'Guts' and attacker.status != 'Healthy' and move.category == 'Physical') or \
		(attacker.currHP <= attacker.stats['hp']/3 and \
			(attacker.ability == 'Overgrow' and move.type == 'Grass') or \
			(attacker.ability == 'Blaze' and move.type == 'Fire') or \
			(attacker.ability == 'Torrent' and move.type == 'Water') or \
			(attacker.ability == 'Swarm' and move.type == 'Bug')):
		atMods.append(1.5)
	elif attacker.ability == 'Flash Fire' and attacker.abilityOn and move.type == 'Fire':
		atMods.append(1.5)
	elif attacker.ability == 'Rocky Payload' and move.type == 'Rock':
		atMods.append(1.5)
	elif attacker.ability == 'Stakeout' and attacker.abilityOn:
		atMods.append(2)
	elif attacker.ability == 'Huge Power' or attacker.ability == 'Pure Power' and move.category == 'Physical':
		atMods.append(2)

	if (defender.ability == 'Thick Fat' and (move.type == 'Fire' or move.type == 'Ice')) or \
		(defender.ability == 'Purifying Salt' and move.type == 'Ghost'):
		atMods.append(0.5)

	isTabletsOfRuinActive = defender.ability == 'Tablets of Ruin' or field.isTabletsOfRuin
	isVesselOfRuinActive = defender.ability == 'Vessel of Ruin' or field.isVesselOfRuin
	if (isTabletsOfRuinActive and move.category == 'Physical') or \
		(isVesselOfRuinActive and move.category == 'Special'):
		atMods.append(0.75)

	if (attacker.ability == 'Protosynthesis' and (field.weather == 'Sun' or attacker.item == 'Booster Energy')) or \
		(attacker.ability == 'Quark Drive' and (field.terrain == 'Electric' or attacker.item == 'Booster Energy')):
		if (move.category == 'Physical' and utils.highestStat(attacker) == 'at') or \
			(move.category == 'Special' and utils.highestStat(attacker) == 'sa'):
			atMods.append(1.3)

	if (attacker.ability == 'Hadron Engine' and move.category == 'Special' and field.terrain == 'Electric' and isGrounded(attacker, field)) or \
		(attacker.ability == 'Orichalcum Pulse' and move.category == 'Physical' and field.weather == 'Sun' and attacker.item != 'Utility Umbrella'):
		atMods.append(4/3)

	if (attacker.item == 'Choice Band' and move.category == 'Physical') or \
		(attacker.item == 'Choice Specs' and move.category == 'Special'):
		atMods.append(1.5)

	return atMods

def calculateDefense(attacker, attackerSide, defender, defenderSide, move, field, isCritical):
	defense = 0

	hitsPhysical = move.overrideDefensiveStat == 'df' or move.category == 'Physical'
	defenseStat = 'df' if hitsPhysical else 'sd'
	if defender.boosts[defenseStat] == 0 or \
		(isCritical and defender.boosts[defenseStat] > 0) or \
		move.ignoreDefensive:
		defense = defender.rawStats[defenseStat]
	elif attacker.ability == 'Unaware':
		defense = defender.rawStats[defenseStat]
	else:
		defense = defender.stats[defenseStat]

	if field.weather == 'Sand' and defender.type == 'Rock' and ~hitsPhysical:
		defense = round(defense*1.5)
	if field.weather == 'Snow' and defender.type == 'Ice' and hitsPhysical:
		defense = round(defense*1.5)

	dfMods = calculateDfMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, hitsPhysical)

	return max(1, round(defense*utils.chainMods(dfMods)))

def calculateDfMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, hitsPhysical):
	dfMods = []

	if defender.ability == 'Marvel Scale' and defender.status != 'Healthy' and hitsPhysical:
		dfMods.append(1.5)
	elif defender.ability == 'Grass Pelt' and field.terrain == 'Grassy' and hitsPhysical:
		dfMods.append(1.5)
	elif defender.ability == 'Fur Coat' and hitsPhysical:
		dfMods.append(2)

	isSwordOfRuinActive = attacker.ability == 'Sword of Ruin' or field.isSwordOfRuin
	isBeadsOfRuinActive = attacker.ability == 'Beads of Ruin' or field.isBeadsOfRuin
	if (isSwordOfRuinActive and hitsPhysical) or \
		(isBeadsOfRuinActive and ~hitsPhysical):
		dfMods.append(0.75)

	if (defender.ability == 'Protosynthesis' and (field.weather == 'Sun' or defender.item == 'Booster Energy')) or \
		(defender.ability == 'Quark Drive' and (field.terrain == 'Electric' or defender.item == 'Booster Energy')):
		if (hitsPhysical and utils.highestStat(defender) == 'df') or \
			(~hitsPhyiscal and utils.highestStat(defender) == 'sd'):
			dfMods.append(1.3)

	if (defender.item == 'Eviolite' and defender.name.nfe) or \
		(~hitsPhysical and defender.item == 'Assault Vest'):
		dfMods.append(1.5)

	return dfMods

def calculateFinalMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, typeEffectiveness):
	finalMods = []

	if defenderSide.isReflect and move.category == 'Physical' and ~isCritical and ~defenderSide.isAuroraVeil:
		finalMods.append(0.5)
	elif defenderSide.isLightScreen and move.category == 'Special' and ~isCritical and ~defenderSide.isAuroraVeil:
		finalMods.append(0.5)
	if defenderSide.isAuroraVeil and ~isCritical:
		finalMods.append(0.5)

	if attacker.ability == 'Tinted Lens' and typeEffectiveness < 1:
		finalMods.append(2)

	if defender.ability == 'Multiscale' and defender.currHP == defender.stats['hp'] and defender.currHP == defender.stats['hp']:
		finalMods.append(0.5)

	if defenderSide.isFriendGuard:
		finalMods.append(0.75)

	if attacker.item == 'Life Orb':
		finalMods.append(1.3)

	return finalMods
