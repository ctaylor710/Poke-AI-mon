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

	attacker = utils.checkSeedBoost(attacker, field)
	defender = utils.checkSeedBoost(defender, field)
	attacker = utils.checkIntimidate(attacker, defender)
	defender = utils.checkIntimidate(attacker, defender)

	attacker.stats = utils.computeFinalStats(attacker, field, attackerSide)
	defender.stats = utils.computeFinalStats(defender, field, defenderSide)

	attacker = utils.checkInfiltrator(attacker)
	defender = utils.checkInfiltrator(defender)

	if attackerSide == 'user':
		attackerSide = field.userSide
		defenderSide = field.opponentSide
	else:
		attackerSide = field.opponentSide
		defenderSide = field.userSide

	result = [0, 0] # [Damage dealt to opponent, damage dealt to self]

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

	noTypeChange = move.name == 'Revelation Dance' or move.name == 'Nature Power' or move.name == 'Terrain Pulse' or (move.name == 'Tera Blast' and attacker.isTera)

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

	fixedDamage = handleFixedDamageMoves(attacker, move)
	if fixedDamage > 0:
		return [fixedDamage, 0]

	if move.name == 'Final Gambit':
		result = [attacker.currHP, attacker.currHP]
		return result

	turnOrder = 'first' if attacker.stats['sp'] > defender.stats['sp'] else 'last'

	basePower = calculateBasePower(attacker, defender, move, field, hasAteAbilityTypeChange)

	if move.bp == 0:
		return result

	attack = calculateAttack(attacker, defender, move, field, isCritical)
	attackSource = defender if move.name == 'Foul Play' else attacker
	if move.name == 'Tera Blast' and attackSource.isTera:
		move.category = 'Physical' if attackSource.stats['at'] > attackSource.stats['sa'] else 'Special'
	attackStat = 'df' if move.name == 'Body Press' else ('sa' if move.category == 'Special' else 'at')

	defense = calculateDefense(attacker, defender, move, field, isCritical)
	hitsPhysical = move.overrideDefensiveStat == 'def' or move.category == 'Physical'
	defenseStat = 'df' if hitsPhysical else 'sd'

	baseDamage = utils.getBaseDamage(attacker.level, basePower, attack, defense)
	

	return result
