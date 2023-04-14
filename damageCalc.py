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
from result import result
import utils

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()
database.addStat()

def UpdateResult(attacker, ally, attackerSide, defender, defender2, defenderSide, move, field, target, result):
	attackerSide.pokes[0] = attacker
	attackerSide.pokes[1] = ally
	defenderSide.pokes[0] = defender
	defenderSide.pokes[1] = defender2
	result.attackerSide = attackerSide
	result.defenderSide = defenderSide
	result.field = field
	result.target = target
	return result

def DamageCalc(attacker, attackerSide, defender, defenderSide, move, field, target, result):

	ally = 0
	defender2 = 0

	if attackerSide == 'user' and defenderSide != 'user':
		attackerSide = field.userSide
		defenderSide = field.opponentSide
		ally = [mon for mon in field.userSide.pokes if mon.name != attacker.name][0]
		defender2 = [mon for mon in field.opponentSide.pokes if mon.name != defender.name][0]
	elif attackerSide != 'user' and defenderSide == 'user':
		attackerSide = field.opponentSide
		defenderSide = field.userSide
		ally = [mon for mon in field.opponentSide.pokes if mon.name != attacker.name][0]
		defender2 = [mon for mon in field.userSide.pokes if mon.name != defender.name][0]
	elif attackerSide == 'user' and defenderSide == 'user':
		attackerSide = field.userSide
		defenderSide = field.userSide
		ally = defender
		defender2 = attacker
	elif attackerSide != 'user' and 'defenderSide' != 'user':
		attackerSide = field.opponentSide
		defenderSide = field.opponentSide
		ally = defender
		defender2 = attacker

	if(attacker.isSwitching == 'in'):
		attacker = utils.checkSeedBoost(attacker, field)
		attacker, ally = utils.switchInChanges(attacker, ally, defender, defender2, attackerSide)
		defender = utils.checkIntimidate(attacker, defender)
		attacker.isSwitching = 'None'
	if(defender.isSwitching == 'in'):
		defender = utils.checkSeedBoost(defender, field)
		defender, defender2 = utils.switchInChanges(defender, defender2, attacker, ally, defenderSide)
		attacker = utils.checkIntimidate(defender, attacker)
		defender.isSwitching = 'None'

	attacker.stats = utils.computeFinalStats(attacker, field, attackerSide)
	ally.stats = utils.computeFinalStats(ally, field, attackerSide)
	defender.stats = utils.computeFinalStats(defender, field, defenderSide)
	defender2.stats = utils.computeFinalStats(defender2, field, defenderSide)

	turnOrder = [(attacker,attacker.stats['sp']), (ally,ally.stats['sp']), (defender,defender.stats['sp']), (defender2,defender2.stats['sp'])]
	turnOrder.sort(key = lambda x: x[1], reverse=True)

	attackerSide = utils.checkInfiltrator(attackerSide)
	defenderSide = utils.checkInfiltrator(defenderSide)

	#result = UpdateResult(attacker, ally, attackerSide, defender, defender2, defenderSide, move, field, target, result)

	if defender.ability == 'Commander' and defender2.name.name == 'Dondozo':
		return result

	if move.category == 'Status' and move.name != 'Nature Power':
		result = applyStatusMoves(attacker, ally, attackerSide, defender, defender2, defenderSide, move, field, result)
		return result
	
	#if move.secondaries and attacker.ability != 'Sheer Force':
	#	result = CalculateSecondaries(result)

	# result = applyStatDrops(attacker, attackerSide, defender, defenderSide, move, field, result)

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
		(move.type == 'Ground' and ~field.gravity and defender.item != 'Iron Ball' and defender.ability == 'Levitate') or \
		(move.isBullet and defender.ability == 'Bulletproof') or \
		(move.isSound and defender.ability == 'Soundproof') or \
		(move.priority > 0 and (defender.ability == 'Dazzling' or defender.ability == 'Armor Tail')) or \
		(move.type == 'Ground' and defender.ability == 'Earth Eater') or \
		(move.isWind and defender.ability == 'Wind Rider'):
		return result

	if move.type == 'Ground' and ~field.gravity and defender.item == 'Air Balloon':
		return result

	if move.priority > 0 and field.terrain == 'Psychic' and utils.isGrounded(defender, field):
		return result

	weightBasedMove = move.name == 'Heat Crash' or move.name == 'Heavy Slam' or move.name == 'Low Kick' or move.name == 'Grass Knot'

	fixedDamage = utils.handleFixedDamageMoves(attacker, move)
	if fixedDamage > 0:
		return [fixedDamage, 0]

	if move.name == 'Final Gambit':
		result = [attacker.currHP, attacker.currHP]
		damage = 0
		if result.attackerSide.pokes[0].name != attacker.name:
			damage = attackerSide.pokes[1].currHP
		else:
			damage = attackerSide.pokes[0].currHP

		result.opponentDamage = damage
		result.selfDamage = damage
		return result

	basePower = CalculateBasePower(attacker, attackerSide, defender, defenderSide, move, field, hasAteAbilityTypeChange)

	if move.bp == 0:
		return result

	attack = CalculateAttack(attacker, attackerSide, defender, defenderSide, move, field, isCritical)
	attackSource = defender if move.name == 'Foul Play' else attacker
	if move.name == 'Tera Blast' and attackSource.isTera:
		move.category = 'Physical' if attackSource.stats['at'] > attackSource.stats['sa'] else 'Special'
	attackStat = 'df' if move.name == 'Body Press' else ('sa' if move.category == 'Special' else 'at')

	defense = CalculateDefense(attacker, attackerSide, defender, defenderSide, move, field, isCritical)
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

	finalMods = CalculateFinalMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, typeEffectiveness)

	protect = False
	if defenderSide.isProtected:
		protect = True

	finalMod = utils.chainMods(finalMods)

	damage = []
	for i in range(16):
		damage.append(utils.getFinalDamage(baseDamage, i, typeEffectiveness, applyBurn, stabMod, finalMod, protect))

	if len(target) == 1:
		if target[0] % 2 == 1:
			result.opponentDamage = damage
		else:
			result.opponent2Damage = damage

	return result

def CalculateBasePower(attacker, attackerSide, defender, defenderSide, move, field, hasAteAbilityTypeChange):
	turnOrder = 'first' if attacker.stats['sp'] > defender.stats['sp'] else 'last'

	basePower = 0

	if move.name == 'Payback':
		basePower = move.bp * (2 if turnOrder == 'last' else 1)
	elif move.name == 'Pursuit':
		switching = defender.isSwitching == 'out'
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
		w = defender.name.weightkg * utils.getWeightFactor(defender)
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

	bpMods = CalculateBPMods(attacker, attackerSide, defender, defenderSide, move, field, basePower, hasAteAbilityTypeChange, turnOrder)
	basePower = max(1, basePower*utils.chainMods(bpMods))

	return basePower

def CalculateBPMods(attacker, attackerSide, defender, defenderSide, move, field, basePower, hasAteAbilityTypeChange, turnOrder):
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
		(move.name == 'Grav Apple' and field.gravity):
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
		(attacker.ability == 'Analytic' and (turnOrder != 'first' or defender.isSwitching == 'out')) or \
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

def CalculateAttack(attacker, attackerSide, defender, defenderSide, move, field, isCritical):
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

	atMods = CalculateAtMods(attacker, attackerSide, defender, defenderSide, move, field)
	attack = round(attack*utils.chainMods(atMods))

	return attack

def CalculateAtMods(attacker, attackerSide, defender, defenderSide, move, field):
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

def CalculateDefense(attacker, attackerSide, defender, defenderSide, move, field, isCritical):
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

	dfMods = CalculateDfMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, hitsPhysical)

	return max(1, round(defense*utils.chainMods(dfMods)))

def CalculateDfMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, hitsPhysical):
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
			(~hitsPhysical and utils.highestStat(defender) == 'sd'):
			dfMods.append(1.3)

	if (defender.item == 'Eviolite' and defender.name.nfe) or \
		(~hitsPhysical and defender.item == 'Assault Vest'):
		dfMods.append(1.5)

	return dfMods

def CalculateFinalMods(attacker, attackerSide, defender, defenderSide, move, field, isCritical, typeEffectiveness):
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

	if defenderSide.friendGuard:
		finalMods.append(0.75)

	if attacker.item == 'Life Orb':
		finalMods.append(1.3)

	return finalMods

def applyStatusMoves(attacker, ally, attackerSide, defender, defender2, defenderSide, move, field, result):

	if attacker.ability == 'Prankster':
		move.priority = 1

	# Section: stat changes to attacker or defender only
	if move.name == 'Belly Drum':
		result.selfStatChanges.append(('at', +12, 101))
		result.selfDamage = round(attacker.currHP/2)

	if move.name in ['Shell Smash', 'Swords Dance']:
		result.selfStatChanges.append(('at', +2, 101))

	if move.name in ['Bulk Up', 'Coil', 'Dragon Dance', 'Growth', 'Hone Claws', 'Howl', 'Meditate', 'Sharpen', 'Shift Gear', 'Work Up']:
		result.selfStatChanges.append(('at', +1, 101))

	if move.name in ['Growl', 'Noble Roar', 'Play Nice', 'Tearful Look', 'Tickle']:
		result.opponentStatChanges.append(('at', -1, 100))

	if move.name == 'Baby-Doll Eyes' and field.terrain != 'Psychic':
		result.opponentStatChanges.append(('at', -1, 100))
		move.priority = 1

	if move.name in ['Charm', 'Feather Dance']:
		result.opponentStatChanges.append(('at', -2, 100))

	if move.name in ['Cotton Guard']:
		result.selfStatChanges.append(('df', +3, 101))

	if (move.name in ['Acid Armor', 'Barrier', 'Iron Defense']) or (move.name == 'Stuff Cheeks' and attacker.item.find('Berry') != -1):
		result.selfStatChanges.append(('df', +2, 101))
		if move.name == 'Stuff Cheeks':
			attacker.item = 'None'

	if move.name in ['Bulk Up', 'Coil', 'Cosmic Power', 'Defense Order', 'Defense Curl', 'Harden', 'Stockpile', 'Withdraw']:
		result.selfStatChanges.append(('df', +1, 101))

	if move.name in ['Screech']:
		result.opponentStatChanges.append(('df', -2, 85))

	if move.name in ['Leer', 'Shell Smash', 'Tail Whip', 'Tickle']:
		result.opponentStatChanges.append(('df', -1, 100))

	if move.name in ['Shell Smash']:
		result.selfStatChanges.append(('df', -1, 101))

	if move.name in ['Nasty Plot', 'Shell Smash']:
		result.selfStatChanges.append(('sa', +2, 101))

	if move.name in ['Calm Mind', 'Growth', 'Quiver Dance', 'Work Up']:
		result.selfStatChanges.append(('sa', +1, 101))

	if move.name in ['Confide', 'Noble Roar', 'Tearful Look']:
		result.opponentStatChanges.append(('sa', -1, 101))

	if move.name in ['Captivate', 'Eerie Impulse']:
		result.opponentStatChanges.append(('sa', -2, 100))

	if move.name in ['Amnesia']:
		result.selfStatChanges.append(('sd', +2, 101))

	if move.name in ['Calm Mind', 'Charge', 'Cosmic Power', 'Defend Order', 'Quiver Dance', 'Stockpile']:
		result.selfStatChanges.append(('sd', +1, 101))

	if move.name in ['Shell Smash']:
		result.selfStatChanges.append(('sd', -1, 101))

	if move.name in ['Fake Tears', 'Metal Sound']:
		result.opponentStatChanges.append(('sd', -2, 100))

	if move.name in ['Agility', 'Autotomize', 'Rock Polish', 'Shell Smash', 'Shift Gear']:
		result.selfStatChanges.append(('sp', +2, 101))

	if move.name in ['Dragon Dance', 'Quiver Dance']:
		result.selfStatChanges.append(('sp', +1, 101))

	if move.name in ['Cotton Spore', 'String shot']:
		result.opponentStatChanges.append(('sp', -2, 100))
		# other opponent lowers

	if move.name in ['Scary Face']:
		result.opponentStatChanges.append(('sp', -2, 100))

	# Section: Secondary Effect
	### Flinch:
	if move.name in ['Bone Club','Extrasensory','Hyper Fang']:
		result.flinch = 10
	if move.name in ['Dark Pulse','Dragon Rush','Fiery Wrath','Twister','Waterfall','Zen Headbutt']:
		result.flinch = 20
	if move.name in ['Air Slash','Astonish','Bite','Double Iron Bash','Floaty Fall','Headbutt','Heart Stamp','Icicle Crash','Iron Head',\
		  'Needle Arm','Rock Slide','Rolling Kick','Sky Attack','Snore','Steamroller','Stomp','Zing Zap']:
		result.flinch = 30
	if move.name in ['Fake Out']:
		result.flinch = 100
	### Burn:
	if move.name in ['Blaze Kick','Ember','Fire Blast','Fire Punch','Flame Wheel','Flamethrower','Flare Blitz','Heat Wave','Ice Burn','Pyro Ball']:
		result.burn = 10
	if move.name in ['Blue Flare']:
		result.burn = 20
	if move.name in ['Lava Plume','Scald','Scorching Sands','Searing Shot','Steam Eruption']:
		result.burn = 30
	if move.name in ['Sacred Fire']:
		result.burn = 50
	if move.name in ['Inferno','Sizzly Slide']:
		result.burn = 100
	### Freeze:
	if move.name in ['Blizzard','Freeze-Dry','Freezing Glare','Ice Beam','Ice Punch','Powder Snow']:
		result.freeze = 10
	### Paralysis
	if move.name in ['Thunder Punch','Thunder Shock','Thunderbolt','Volt Tackle']:
		result.paralysis = 10
	if move.name in ['Bolt Strike']:
		result.paralysis = 20
	if move.name in ['Body Slam','Bounce','Discharge','Dragon Breath','Force Palm','Freeze Shock','Lick','Spark','Splishy Splash','Thunder']:
		result.paralysis = 30
	if move.name in ['Buzzy Buzz','Nuzzle','Stoked Sparksurfer','Zap Cannon']:
		result.paralysis = 100
	### Confusion
	if move.name in ['Confusion','Psybeam','Signal Beam']:
		result.confusion = 10
	if move.name in ['Dizzy Punch','Rock Climb','Strange Steam','Water Pulse']:
		result.confusion = 20
	if move.name in ['Hurricane']:
		result.confusion = 30
	if move.name in ['Chatter','Dynamic Punch']:
		result.confusion = 100
	### Poison
	if move.name in ['Cross Poison','Poison Tail','Sludge Wave']:
		result.poison = 10
	if move.name in ['Shell Side Arm','Twineedle']:
		result.poison = 20
	if move.name in ['Gunk Shot','Poison Jab','Poison Sting','Sludge','Sludge Bomb']:
		result.poison = 30
	if move.name == 'Smog':
		result.poison = 40
	### Bad Poison/toxic
	if move.name == 'Poison Fang':
		result.toxic = 50
	### Sleep:
	if move.name in ['Relic Song']:
		result.sleep = 10
	### Prevent Sound:
	if move.name in ['Throat Chop']:
		result.sleep = 100
	### Double Effect
	if move.name == 'Fire Fang':
		result.flinch = 10
		result.burn = 10
	if move.name == 'Ice Fang':
		result.flinch = 10
		result.freeze = 10
	if move.name == 'Thunder Fang':
		result.flinch = 10
		result.paralysis = 10
	### Triple Effect
	if move.name == 'Tri Attack':
		result.burn = 6.67
		result.freeze = 6.67
		result.paralysis = 6.67
	
	### Trap:
	if move.name in ['Anchor Shot','Spirit Shackle']:
		result.traps = True

	### Lowering attack:
	if move.name in ['Aurora Beam','Play Rough']:
		result.opponentStatChanges.append(('at', -1, 10))
	if move.name in ['Breaking Swipe','Lunge','Trop Kick']:
		result.opponentStatChanges.append(('at', -1, 100))
	### Lowering defense:
	if move.name in ['Iron Tail']:
		result.opponentStatChanges.append(('df', -1, 10))
	if move.name in ['Crunch','Liquidation','Shadow Bone']:
		result.opponentStatChanges.append(('df', -1, 20))
	if move.name in ['Crush Claw','Razor Shell','Rock Smash']:
		result.opponentStatChanges.append(('df', -1, 50))
	if move.name in ['Fire Lash','Grav Apple','Thunderous Kick']:
		result.opponentStatChanges.append(('df', -1, 100))
	### Lowering SA:
	if move.name in ['Moonblast']:
		result.opponentStatChanges.append(('sa', -1, 30))	
	if move.name in ['Mist Ball']:
		result.opponentStatChanges.append(('sa', -1, 50))
	if move.name in ['Mystical Fire','Skitter Smack','Snarl','Spirit Break','Struggle Bug']:
		result.opponentStatChanges.append(('sa', -1, 100))
	### Lowering SD:
	if move.name in ['Acid','Bug Buzz','Earth Power','Energy Ball','Flash Cannon','Focus Blast','Psychic']:
		result.opponentStatChanges.append(('sd', -1, 10))
	if move.name == 'Shadow Ball':
		result.opponentStatChanges.append(('sd', -1, 20))
	if move.name == 'Luster Purge':
		result.opponentStatChanges.append(('sd', -1, 50))
	if move.name == 'Apple Acid':
		result.opponentStatChanges.append(('sd', -1, 100))
	if move.name == 'Seed Flare':
		result.opponentStatChanges.append(('sd', -2, 40))
	if move.name == 'Acid Spray':
		result.opponentStatChanges.append(('sd', -2, 100))
	### Lowering speed:
	if move.name in ['Bubble','Bubble Beam','Constrict']:
		result.opponentStatChanges.append(('sp', -1, 10))
	if move.name in ['Bulldoze','Drum Beating','Electroweb','Glaciate','Icy Wind','Low Sweep','Mud Shot','Rock Tomb']:
		result.opponentStatChanges.append(('sp', -1, 100))

	### Buff AT:
	if move.name in ['Metal Claw']:
		result.selfStatChanges.append(('at', +1, 10))
	if move.name in ['Meteor Mash']:
		result.selfStatChanges.append(('at', +1, 20))
	if move.name in ['Meteor Mash','Power-Up Punch']:
		result.selfStatChanges.append(('at', +1, 100))
	### Buff DF:
	if move.name in ['Steel Wing']:
		result.selfStatChanges.append(('df', +1, 10))
	if move.name in ['Diamond Storm']:
		result.selfStatChanges.append(('df', +2, 50))
	### Buff SA:
	if move.name in ['Fiery Dancez']:
		result.selfStatChanges.append(('sa', +1, 50))
	if move.name in ['Charge Beam']:
		result.selfStatChanges.append(('sa', +1, 70))
	### Buff SP:
	if move.name in ['Aura Wheel','Flame Charge']:
		result.selfStatChanges.append(('sp', +1, 100))

	### Buff all:
	if move.name in ['Ancient Power','Ominous Wind','Silver Wind']:
		result.selfStatChanges.append(('at', +1, 10))
		result.selfStatChanges.append(('df', +1, 10))
		result.selfStatChanges.append(('sa', +1, 10))
		result.selfStatChanges.append(('sd', +1, 10))
		result.selfStatChanges.append(('sp', +1, 10))
	if move.name == 'Clangorous Soulblaze':
		result.selfStatChanges.append(('at', +1, 100))
		result.selfStatChanges.append(('df', +1, 100))
		result.selfStatChanges.append(('sa', +1, 100))
		result.selfStatChanges.append(('sd', +1, 100))
		result.selfStatChanges.append(('sp', +1, 100))

	### Change Terrain:
	if move.name == 'Genesis Supernova':
		result.field.terrain = 'Psychic'


	
	
	
	
						



	# Section: stat changes for double battles
	if move.name == 'Aurora Veil':
		result.attackerSide.isAuroraVeil = True

	if move.name == 'Reflect':
		result.attackerSide.isReflect = True

	if move.name == 'Light Screen':
		result.attackerSide.isLightScreen = True

	if move.name == 'Defog':
		result.defenderSide.isReflect = False
		result.defenderSide.isLightScreen = False

	if move.name == 'Electric Terrain':
		result.field.terrain == 'Electric'

	if move.name == 'Psychic Terrain':
		result.field.terrain = 'Psychic'

	if move.name == 'Grassy Terrain':
		result.field.terrain = 'Grassy'

	if move.name == 'Misty Terrain':
		result.field.terrain = 'Misty'

	if move.name == 'Encore':
		result.defender.isEncored = True

	if move.name == 'Follow Me':
		result.attacker.isFollowMe = True

	if move.name == 'Gravity':
		result.field.gravity = True

	if move.name == 'Haze':
		for stat in attacker.stats.keys():
			result.attackerSide.pokes[0].boosts[stat] = 0
			result.attackerSide.pokes[1].boosts[stat] = 0
			result.defenderSide.pokes[0].boosts[stat] = 0
			result.attackerSide.pokes[1].boosts[stat] = 0

	if move.name == 'Helping Hand':
		attackerSide.isHelpingHand = True

	if move.name == 'Trick Room':
		field.trickRoom = True
		result.turnOrder.sort(key = lambda x: x[1])

	# Section: protecting moves
	if move.name in ['Protect', 'Detect']:
		result.attackerSide.isProtected = True

	if move.name == 'Wide Guard':
		result.attackerSide.isWideGuard = True

	if move.name == 'Quick Guard':
		result.attackerSide.isQuickGuard = True

	result.attacker = attacker
	result.attackerSide = attackerSide
	result.defender = defender
	result.defenderSide = defenderSide
	result.field = field

	return result


def CalculateSecondaries(move, result):
	return 0

# This function captures the dynamics of our environment. The dynamics are a mix of deterministic and stochastic results;
# most damage moves deal damage within a range of numbers, while status moves always have fixed effects. That being said,
# the stochastic dynamics of the environment can be treated as deterministic by looking at 'best-case', 'average', and 'worst-case'
# scenarios (these scenarios are deterministic depending on the action being taken, and so there is never doubt in what defines each scenario)
def TakeMove(attacker, attackerSide, defender, defenderSide, move, field, target):
	ally = 0
	defender2 = 0
	myResult = result()
	if attackerSide == 'user' and defenderSide != 'user':
		ally = [mon for mon in field.userSide.pokes if mon.name != attacker.name][0]
		defender2 = [mon for mon in field.opponentSide.pokes if mon.name != defender.name][0]
	elif attackerSide != 'user' and defenderSide == 'user':
		ally = [mon for mon in field.opponentSide.pokes if mon.name != attacker.name][0]
		defender2 = [mon for mon in field.userSide.pokes if mon.name != defender.name][0]
	elif attackerSide == 'user' and defenderSide == 'user':
		ally = defender
		defender2 = attacker
	elif attackerSide != 'user' and 'defenderSide' != 'user':
		ally = defender
		defender2 = attacker
	if move == 'Switch':
		attacker.isSwitching = 'out'
		defender.isSwitching = 'in'
		myResult.attacker = attacker
		myResult.defender = defender
		return myResult
	if (attacker.item.find('Choice') != -1 and move != attacker.lastMove and attacker.lastMove.name != 'None') or \
		(attacker.item == 'Assault Vest' and move.category == 'Status'):
		return myResult
	print('target', target)
	print('move', move.name)
	myResult = DamageCalc(attacker, attackerSide, defender, defenderSide, move, field, target, myResult)
	print('opp1', myResult.opponentDamage)
	print('opp2', myResult.opponent2Damage)
	return myResult


