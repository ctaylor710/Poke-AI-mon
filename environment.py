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
import pickle

database = database()
database.addMoves()
database.addTypes()
database.addSpecies()
database.addNatures()
# Tables used to encode and decode strings into integers and vice versa
def typeTable():
	return {0:'None', 1:'Normal', 2:'Fire', 3:'Water', 4:'Grass', 5:'Electric', 6:'Ice', 7:'Fighting', 8:'Poison', \
			8:'Ground', 9:'Flying', 10:'Psychic', 11:'Bug', 12:'Rock', 13:'Ghost', 14:'Dark', 15:'Dragon', \
			16:'Steel', 17:'Fairy'}

def categoryTable():
	return {0:'Status', 1:'Physical', 2:'Special'}

def targetTable():
	return {0:'Adjacent', 1:'AdjacentAlly', 2:'AdjacentAllyOrSelf', 3:'AdjacentFoe', 4:'AllAdjacentFoes', 5:'Allies', 6:'All', 7:'Self'}

def itemTable():
	return {0:'Ability Shield', 1:'Focus Sash', 2:'Bright Powder', 3:'Weakness Policy', 4:'Eject Button', 5:'Iron Ball', 6:'Safety Goggles', 7:'Terrain Extender', \
		8:'Light Clay', 9:'Choice Band', 10:'Choice Specs', 11:'Choice Scarf', 12:'Heavy-Duty Boots', 13:'Rocky Helmet', 14:'Expert Belt', 15:'Zoom Lens', \
		16:'Life Orb', 17:'Sitrus Berry', 18:'Assault Vest', 19:'Leftovers', 20:'Lum Berry', 21:'Air Balloon', 22:'Charcoal', 23:'Booster Energy', \
		24:'Psychic Seed', 25:'Twisted Spoon', 26:'Mystic Water', 27:'Dragon Fang', 28:'Covert Clock', 29:'Clear Amulet', 30:'Black Sludge', 31:'Red Card', \
		32:'Babiri Berry', 33:'Charti Berry', 34:'Chilan Berry', 35:'Chople Berry', 36:'Coba Berry', 37:'Colbur Berry', 38:'Haban Berry', 39:'Kasib Berry', \
		40:'Kebia Berry', 41:'Occa Berry', 42:'Passho Berry', 43:'Payapa Berry', 44:'Rindo Berry', 45:'Roseli Berry', 46:'Shuca Berry', 47:'Tanga Berry', \
		48:'Wacan Berry', 49:'Yache Berry', 50:'Mirror Herb', 51:'Mental Herb', 52:'Loaded Dice'}

def abilityTable():
	return {0:'Adaptability', 1:'Aerilate', 2:'Aftermath', 3:'Air Lock', 4:'Analytic', 5:'Anger Point', 6:'Anger Shell', 7:'Anticipation', \
		8:'Arena Trap', 9:'Armor Tail', 10:'Aroma Veil', 11:'As One', 12:'Aura Break', 13:'Bad Dreams', 14:'Ball Fetch', 15:'Battery', \
		16:'Battle Armor', 17:'Battle Bond', 18:'Beads of Ruin', 19:'Beast Boost', 20:'Berserk', 21:'Big Pecks', 22:'Blaze', 23:'Bulletproof', \
		24:'Cheek Pouch', 25:'Chilling Neigh', 26:'Chlorophyll', 27:'Clear Body', 28:'Cloud Nine', 29:'Color Change', 30:'Comatose', 31:'Commander', \
		32:'Competitive', 33:'Compound Eyes', 34:'Contrary', 35:'Corrosion', 36:'Costar', 37:'Cotton Down', 38:'Cud Chew', 39:'Curious Medicine', \
		40:'Cursed Body', 41:'Cute Charm', 42:'Damp', 43:'Dancer', 44:'Dark Aura', 45:'Dauntless Shield', 46:'Dazzling', 47:'Defeatist', \
		48:'Defiant', 49:'Delta Stream', 50:'Desolate Land', 51:'Disguise', 52:'Download', 53:'Dragon\'s maw', 54:'Drizzle', 55:'Drought', \
		56:'Dry Skin', 57:'Early Bird', 58:'Earth Eater', 59:'Effect Spore', 60:'Electric Surge', 61:'Electromorphosis', 62:'Emergency Exit', 63:'Fairy Aura', \
		64:'Filter', 65:'Flame Body', 66:'Flare Boost', 67:'Flash Fire', 68:'Flower Gift', 69:'Flower Veil', 70:'Fluffy', 71:'Forecast', \
		72:'Forewarn', 73:'Friend Guard', 74:'Frisk', 75:'Full Metal Body', 76:'Fur Coat', 77:'Gale Wings', 78:'Galvanize', 79:'Gluttony', \
		80:'Good as Gold', 81:'Gorilla Tactics', 82:'Grass Pelt', 83:'Grassy Surge', 84:'Grim Neigh', 85:'Guard Dog', 86:'Gulp Missile', 87:'Guts', \
		88:'Hadron Engine', 89:'Harvest', 90:'Healer', 91:'Heatproof', 92:'Heavy Metal', 93:'Honey Gather', 94:'Huge Power', 95:'Hunger Switch', \
		96:'Hustle', 97:'Hydration', 98:'Hyper Cutter', 99:'Ice Body', 100:'Ice Face', 101:'Ice Scales', 102:'Illuminate', 103:'Illusion', \
		104:'Immunity', 105:'Imposter', 106:'Infiltrator', 107:'Innards Out', 108:'Inner Focus', 109:'Insomnia', 110:'Intimidate', 111:'Intrepid Sword', \
		112:'Iron Barbs', 113:'Iron Fist', 114:'Justified', 115:'Keen Eye', 116:'Klutz', 117:'Leaf Guard', 118:'Levitate', 119:'Libero', \
		120:'Light Metal', 121:'Lightning Rod', 122:'Limber', 123:'Lingering Aroma', 124:'Liquid Ooze', 125:'Liquid Voice', 126:'Long Reach', 127:'Magic Bounce', \
		128:'Magician', 129:'Magma Armor', 130:'Magnet Pull', 131:'Marvel Scale', 132:'Mega Launcher', 133:'Merciless', 134:'Mimicry', 135:'Minus', \
		136:'Mirror Armor', 137:'Misty Surge', 138:'Mold Breaker', 139:'Moody', 140:'Motor Drive', 141:'Moxie', 142:'Multiscale', 143:'Multitype', \
		144:'Mummy', 145:'Mycelium Might', 146:'Natural Cure', 147:'Neuroforce', 148:'Neutralizing Gas', 149:'No Guard', 150:'Normalize', 151:'Oblivious', \
		152:'Opportunist', 153:'Orichalcum Pulse', 154:'Overcoat', 155:'Overgrow', 156:'Own Tempo', 157:'Parental Bond', 158:'Pastel Veil', 159:'Perish Body', \
		160:'Pickpocket', 161:'Pickup', 162:'Pixilate', 163:'Plus', 164:'Poison Heal', 165:'Poison Point', 166:'Poison Touch', 167:'Power Construct', \
		168:'Power of Alchemy', 169:'Power Spot', 170:'Prankster', 171:'Pressure', 172:'Primordial Sea', 173:'Prism Armor', 174:'Propellor Tail', 175:'Protean', \
		176:'Protosynthesis', 177:'Pyschic Surge', 178:'Punk Rock', 179:'Pure Power', 180:'Purifying Salt', 181:'Quark Drive', 182:'Queenly Magesty', 183:'Quick Draw', \
		184:'Quick Feet', 185:'Rain Dish', 186:'Rattled', 187:'Receiver', 188:'Reckless', 189:'Refrigerate', 190:'Regenerator', 191:'Ripen', \
		192:'Rivalry', 193:'RKS System', 194:'Rock Head', 195:'Rocky Payload', 196:'Rough Skin', 197:'Run Away', 198:'Sand Force', 199:'Sand Rush', \
		200:'Sand Spit', 201:'Sand Stream', 202:'Sand Veil', 203:'Sap Sipper', 204:'Schooling', 205:'Scrappy', 206:'Screen Cleaner', 207:'Seed Power', \
		208:'Serene Grace', 209:'Shadow Shield', 210:'Shadow Tag', 211:'Sharpness', 212:'Shed Skin', 213:'Sheer Force', 214:'Shell Armor', 215:'Shield Dust', \
		216:'Shields Down', 217:'Simple', 218:'Skill Link', 219:'Slow Start', 220:'Slush Rush', 221:'Sniper', 222:'Snow Cloak', 223:'Snow Warning', \
		224:'Solar Power', 225:'Solid Rock', 226:'Soul-Heart', 227:'Soundproof', 228:'Speed Boost', 229:'Stakeout', 230:'Stall', 231:'Stalwart', \
		232:'Stall', 233:'Stamina', 234:'Stance Change', 235:'Static', 236:'Steadfast', 237:'Steam Engine', 238:'Steelworker', 239:'Steely Spirit', \
		240:'Stench', 241:'Sticky Hold', 242:'Storm Drain', 243:'Strong Jaw', 244:'Sturdy', 245:'Suction Cups', 246:'Super Luck', 247:'Supreme Overlord', \
		248:'Surge Surfer', 249:'Swarm', 250:'Sweet Veil', 251:'Swift Swim', 252:'Sword of Ruin', 253:'Symbiosis', 254:'Synchronize', 255:'Tablets of Ruin', \
		256:'Tangled Feet', 257:'Tangling Hair', 258:'Technician', 259:'Telepathy', 260:'Teravolt', 261:'Thermal Exchange', 262:'Thick Fat', 263:'Tinted Lens', \
		264:'Torrent', 265:'Tough Claws', 266:'Toxic Boost', 267:'Toxic Debris', 268:'Trace', 269:'Transistor', 270:'Triage', 271:'Truant', \
		272:'Turboblaze', 273:'Unaware', 274:'Unburden', 275:'Unnerve', 276:'Unseen Fist', 277:'Vessel of Ruin', 278:'Victory Star', 279:'Vital Spirit', \
		280:'Volt Absorb', 281:'Wandering Spirit', 282:'Water Absorb', 283:'Water Bubble', 284:'Water Compaction', 285:'Water Veil', 286:'Weak Armor', \
		288:'Well-Baked Body', 289:'White Smoke', 290:'Wimp Out', 291:'Wind Power', 292:'Wind Rider', 293:'Wonder Guard', 294:'Wonder Skin', 295:'Zen Mode', \
		296:'Zero to Hero'}

def MoveTargets(move):
	if move.target != 'Adjacent': # This means the targeting was specified in the database, so we're good
		return move.target
	else:
		if move.name in ['Acid Armor', 'Agility', 'Ally Switch', 'Amnesia', 'Aqua Ring', 'Assist', 'Autotomize', 'Baneful Bunker', \
			'Barrier', 'Baton Pass', 'Bulk Up', 'Calm Mind', 'Camouflage', 'Celebrate', 'Charge', 'Clangorous Soul', 'Coil', \
			'Conversion', 'Copycat', 'Cosmic Power', 'Cotton Guard', 'Curse', 'Defend Order', 'Defense Curl', 'Destiny Bond', \
			'Detect', 'Double Team', 'Dragon Dance', 'Endure', 'Focus Energy', 'Follow Me', 'Geomancy', 'Growth', 'Grudge', \
			'Harden', 'Heal Order', 'Healing Wish', 'Hone Claws', 'Howl', 'Imprison', 'Ingrain', 'Iron Defense', 'Laser Focus', \
			'Lunar Dance', 'Magic Coat', 'Magnet Rise', 'Meditate', 'Metronome', 'Milk Drink', 'Minimize', 'Moonlight', 'Morning Sun', \
			'Nasty Plot', 'No Retreat', 'Obstruct', 'Power Trick', 'Protect', 'Quiver Dance', 'Rage Powder', 'Recover', 'Recycle', \
			'Refresh', 'Rest', 'Rock Polish', 'Roost', 'Sharpen', 'Shell Smash', 'Shift Gear', 'Shore Up', 'Slack Off', 'Sleep Talk', \
			'Snatch', 'Soft-Boiled', 'Spiky Shield', 'Splash', 'Stockpile', 'Stuff Cheeks', 'Substitute', 'Swallow', 'Swords Dance', \
			'Synthesis', 'Tail Glow', 'Teleport', 'Wish', 'Withdraw', 'Work Up']:
			return 'Self'
		elif move.name in ['Acupressure']:
			return 'AdjacentAllyOrSelf'
		elif move.name in ['Aromatherapy', 'Aurora Veil', 'Crafty Shield', 'Gear Up', 'Happy Hour', 'Heal Bell', 'Jungle Healing', \
			'Life Dew', 'Light Screen', 'Lucky Chant', 'Magnetic Flux', 'Mat Block', 'Mist', 'Quick Guard', 'Reflect', 'Safeguard', \
			'Tailwind', 'Wide Guard']:
			return 'Allies'
		elif move.name in ['Aromatic Mist', 'Helping Hand', 'Hold Hands']:
			return 'AdjacentAlly'
		elif move.name in ['Captivate', 'Cotton Spore', 'Dark Void', 'Growl', 'Heal Block', 'Leer', 'Poison Gas', 'Spikes', 'Stealth Rock', \
			'Sticky Web', 'String Shot', 'Sweet Scent', 'Tail Whip', 'Toxic Spikes', 'Venom Drench']:
			return 'AllAdjacentFoes'
		elif move.name in ['Corrosive Gas', 'Teeter Dance']:
			return 'AllAdjacent'
		elif move.name in ['Court Change', 'Electric Terrain', 'Fairy Lock', 'Flower Shield', 'Grassy Terrain', 'Gravity', 'Snowscape', \
			'Haze', 'Ion Deluge', 'Magic Room', 'Misty Terrain', 'Mud Sport', 'Perish Song', 'Psychic Terrain', 'Rain Dance', 'Rototiller', \
			'Sandstorm', 'Sunny Day', 'Teatime', 'Trick Room', 'Water Sport', 'Wonder Room']:
			return 'All'
		else:
			return move.target

def LoadTeam(fileName):
	team = []
	file = open(f'pokemonFiles/{fileName}')
	index = -1
	for line in file:
		line = line.strip()
		if len(line) > 0:
			words = line.split('@')
			words[0] = words[0].strip()
			if words[0] in database.speciesDict.keys():
				team.append(pokemon())
				index += 1
		team[-1].addDataLine(database, line)
	return team
	file.close()

def CreateEnv():
	fileName = 'TestTeam.txt' #input('Enter your team sheet: ')
	userTeam = LoadTeam(fileName)
	fileName = 'TestTeam.txt' #input('Enter opponent team sheet: ')
	opponentTeam = LoadTeam(fileName)
	return userTeam, opponentTeam

# This AI is used to help us create more meaningful demonstrations. In essence, all it does is chooses the move that will deal
# the most damage on an HP basis to the opposing team. The idea is that, if I start the game in an unfavorable matchup, the AI will
# still be able to push their advantage, albeit in a predictable way.
def maxDamageAI(pokemon, ally, opposingSide, field):
	maxDamage = 0
	maxDamageMove = 0
	bestTarget = []
	for move in pokemon.moves:
		totalDamage = 0
		if move.target in ['Adjacent', 'AdjacentFoe']:
			for i in range(len(opposingSide.pokes)):
				target = [i+1]
				moveResult = result()
				moveResult = damageCalc.TakeMove(pokemon, 'opponent', opposingSide.pokes[i], 'user', move, field, target[0], moveResult)
				totalDamage = moveResult.opponentDamage[-1] + moveResult.opponent2Damage[-1]
				if totalDamage > maxDamage:
					maxDamage = totalDamage
					maxDamageMove = move
					bestTarget = target
		elif move.target in ['AllAdjacentFoe', 'AllAdjacent']:
			if len(opposingSide.pokes) > 1:
				result1 = result()
				result1 = damageCalc.TakeMove(pokemon, 'opponent', opposingSide.pokes[0], 'user', move, field, 1, result1)
				result2 = result()
				result2 = damageCalc.TakeMove(pokemon, 'opponent', opposingSide.pokes[1], 'user', move, field, 2, result2)
				if move.target == 'AllAdjacentFoe':
					target = [1, 2]
				else:
					allyPos = 3 if field.opponentSide.pokes[0].name.name == pokemon.name.name else 4
					target = [1, 2, allyPos]
				totalDamage = result1.opponentDamage[-1] + result2.opponent2Damage[-1]
			else:
				moveResult = result()
				moveResult = damageCalc.TakeMove(pokemon, 'opponent', opposingSide.pokes[0], 'user', move, field, 1, moveResult)
				target = [1]
				totalDamage = moveResult.opponentDamage[-1] + moveResult.opponent2Damage[-1]
			if totalDamage > maxDamage:
				maxDamage = totalDamage
				maxDamageMove = move
				bestTarget = target

	return maxDamageMove, bestTarget

# We will define our state vector using the following format:
#	We start by embedding the 2 pokemon we have on the field into the vector, followed by the 2 pokemon we have in the back
#		For each pokemon, we include the following information in the following order:
#			- their type will be embedded as a vector, each number corresponds to a type (see EncodePokeInfo)
#			- stats
#			- stat boosts
#			- current hp
#			- items will be embedded as a number (see EncodePokeInfo)
#			- the same goes for abilities
#			- the tera type will be embedded as a number, following the same system as regular typing
#			- this is followed by a boolean indicating whether the pokemon is terrastallized
#			- next is a vector containing their EVs. The order is the same as that found in the pokemon class
#			- IVs
#			- level is omitted; all pokemon will be level 50
#			- nature is embedded as a vector of 1's, with the raised stat being 1.1, the lowered being 0.9
#			- each move is embedded as a list of its properties (for more information, see EncodeMoveInfo) * Note that we are not considering move accuracy, which is one of the biggest drawbacks right now
#			- the last move the pokemon used is also embedded in this manner. If this is their first turn, this vector is left empty
#			- pokemon status is embedded as a number corresponding to their status' index (see moves.statusList)
#			- their switching status is as follows: 0:no change, 1:in, 2:out
#			- we include if the pokemon is encored or 'follow me'ed as booleans
#	Next, we include the 2 pokemon the opponent has on the field, followed by the 2 pokemon they have in the back
#		Same process of embedding data
#	We then embed any field effects
#		We mostly just include all the effects from our field class
#		However, we do embed the data about both sides after field effects

def EncodeMoveInfo(move):
	moveVec = []

	moveVec.append(move.bp)

	typeTableCopy = typeTable()
	for types in typeTableCopy.keys():
		if typeTableCopy[types] == move.type:
			moveVec.append(types)

	categoryTableCopy = categoryTable()
	for category in categoryTableCopy.keys():
		if categoryTableCopy[category] == move.category:
			moveVec.append(category)

	moveVec.append(move.multihit)

	moveVec.append(move.drain)

	moveVec.append(move.recoil)

	moveVec.append(move.priority)

	## ERROR HERE
	targetTableCopy = targetTable()
	for target in targetTableCopy.keys():
		if targetTableCopy[target] == move.target:
			moveVec.append(target)

	moveVec.append(move.makesContact)

	moveVec.append(move.isPunch)

	moveVec.append(move.isSound)

	moveVec.append(move.isPulse)

	moveVec.append(move.isBite)

	moveVec.append(move.isWind)

	moveVec.append(move.isSlicing)

	moveVec.append(move.willCrit)

	return moveVec


def EncodePokeInfo(pokemon):
	pokeVec = []

	typeTableCopy = typeTable()
	for types in typeTableCopy.keys():
		if typeTableCopy[types] in pokemon.name.types:
			pokeVec.append(types)
	if len(pokemon.name.types) == 1: # If a pokemon is monotype, their second typing is 'None' to maintain vector shape
		pokeVec.append(0)

	for stat in pokemon.stats.keys():
		pokeVec.append(pokemon.stats[stat])

	for boost in pokemon.boosts.keys():
		pokeVec.append(pokemon.boosts[boost])

	pokeVec.append(pokemon.currHP)

	itemTableCopy = itemTable()
	for item in itemTableCopy.keys():
		if itemTableCopy[item] == pokemon.item:
			pokeVec.append(item)
			continue

	abilityTableCopy = abilityTable()

	for ability in abilityTableCopy.keys():
		if abilityTableCopy[ability] == pokemon.ability:
			pokeVec.append(ability)
			continue

	for types in typeTableCopy.keys():
		if typeTableCopy[types] == pokemon.tera:
			pokeVec.append(types)
			continue

	pokeVec.append(pokemon.isTera)

	for stat in pokemon.EVs.keys():
		pokeVec.append(pokemon.EVs[stat])

	for stat in pokemon.IVs.keys():
		pokeVec.append(pokemon.IVs[stat])

	for stat in pokemon.natureBoosts.keys():
		pokeVec.append(pokemon.natureBoosts[stat])

	for move in pokemon.moves:
		pokeVec.append(EncodeMoveInfo(move))

	pokeVec.append(EncodeMoveInfo(pokemon.lastMove))

	switchTable = {0:'None', 1:'in', 2:'out'}
	for switch in switchTable.keys():
		if switchTable[switch] == pokemon.isSwitching:
			pokeVec.append(switch)
			continue

	pokeVec.append(pokemon.isEncored)

	pokeVec.append(pokemon.isFollowMe)

	pokeVec.append(pokemon.isProtected)

	return pokeVec

def EncodeFieldInfo(field):
	fieldVec = []

	for i in range(len(field.weatherList)):
		if field.weatherList[i] == field.weather:
			fieldVec.append(i)

	for i in range(len(field.terrainList)):
		if field.terrainList[i] == field.terrain:
			fieldVec.append(i)

	fieldVec.append(field.trickRoom)

	fieldVec.append(field.trickRoomTurns)

	fieldVec.append(field.isBeadsOfRuin)

	fieldVec.append(field.isSwordOfRuin)

	fieldVec.append(field.isTabletsOfRuin)

	fieldVec.append(field.isVesselOfRuin)

	return fieldVec

def EncodeSideInfo(side):
	sideVec = []

	sideVec.append(side.isReflect)
	sideVec.append(side.reflectTurns)

	sideVec.append(side.isLightScreen)
	sideVec.append(side.lightScreenTurns)

	sideVec.append(side.tailwind)
	sideVec.append(side.tailwindTurns)

	sideVec.append(side.isAuroraVeil)
	sideVec.append(side.auroraVeilTurns)

	sideVec.append(side.friendGuard)

	sideVec.append(side.isWideGuard)

	sideVec.append(side.isQuickGuard)

	sideVec.append(side.isHelpingHand)

	sideVec.append(len(side.availablePokes))

	return sideVec

def StateVector(field, userPokes, opponentPokes):
	stateVec = []
	for pokes in userPokes:
		stateVec.append(EncodePokeInfo(pokes))
	for pokes in opponentPokes:
		stateVec.append(EncodePokeInfo(pokes))
	stateVec.append(EncodeFieldInfo(field))
	stateVec.append(EncodeSideInfo(field.userSide))
	stateVec.append(EncodeSideInfo(field.opponentSide))

	return stateVec

# We will define our action vector using the following format:
#	The 4 actions taken by each pokemon will be preceded by the order in which they occur; the pokemon to move first is given 1, the bext pokemon is given 2, and so on
#	We define the possible targets in the following way:
#		The targets of the move is listed as a vector. The vector may contain the numbers 0-8, inclusive.
#		If the player is attacking, the numbers included in the vector correspond to the order in which the pokes vector is listed in TakeAction().
#			Thus, these can be any numbers between 1-4. The constraints on what numbers can actually be used for which move is determined in a higher-level module
#		If the player is switching, the vector is started with the number 0 to indicate this, followed by a number from 5-8 to indicate which pokemon they are switching with
#			Again, order is determined by the availablePokes vector passed in
# We then pass in the quantitative results of taking that move. Note that this is different from dynamics: the action is the damage, healing, etc. that results from taking that
# move, and the dynamics is adding these quantitative results to the current state and updating it
def actionVector(result):
	actionVec = []

	actionVec.append(result.user)
	actionVec.append(result.target)

	actionVec.append(EncodeFieldInfo(result.field))
	if result.attackerSide.side == 'user':
		actionVec.append(EncodeSideInfo(result.attackerSide))
		actionVec.append(EncodeSideInfo(result.defenderSide))
		if result.user == 0:
			actionVec.append([result.selfDamage])
			actionVec.append(result.allyDamage)
		else:
			actionVec.append(result.allyDamage)
			actionVec.append([result.selfDamage])

		actionVec.append(result.opponentDamage)
		actionVec.append(result.opponent2Damage)

		if result.user == 0:
			actionVec.append(result.selfStatChanges)
			actionVec.append(result.allyStatChanges)
		else:
			actionVec.append(result.allyStatChanges)
			actionVec.append(result.selfStatChanges)

		actionVec.append(result.opponentStatChanges)
		actionVec.append(result.opponent2StatChanges)

	else:
		actionVec.append(EncodeSideInfo(result.defenderSide))
		actionVec.append(EncodeSideInfo(result.attackerSide))
		
		actionVec.append(result.opponentDamage)
		actionVec.append(result.opponent2Damage)
		if result.user == 2:
			actionVec.append([result.selfDamage])
			actionVec.append(result.allyDamage)
		else:
			actionVec.append(result.allyDamage)
			actionVec.append([result.selfDamage])

		actionVec.append(result.opponentStatChanges)
		actionVec.append(result.opponent2StatChanges)

		if result.user == 2:
			actionVec.append(result.selfStatChanges)
			actionVec.append(result.allyStatChanges)
		else:
			actionVec.append(result.allyStatChanges)
			actionVec.append(result.selfStatChanges)


	actionVec.append(result.protects)
	actionVec.append(result.flinch)
	actionVec.append(result.traps)
	actionVec.append(result.burn)
	actionVec.append(result.freeze)
	actionVec.append(result.paralysis)
	actionVec.append(result.poison)
	actionVec.append(result.toxic)
	actionVec.append(result.sleep)
	actionVec.append(result.confusion)
	actionVec.append(result.preventsSound)

	moveIndex = 4
	if result.user < 2:
		poke = result.field.userSide.pokes[result.user]
	else:
		poke = result.field.opponentSide.pokes[result.user-2]
	for i in range(len(poke.moves)):
		if poke.moves[i].name == result.move.name:
			moveIndex = i
	actionVec.append(moveIndex)


	return actionVec


def TakeAction(field, pokes, moves, targets, availablePokes, repeat):
	actionVec = []

	turnOrder = [[pokes[0], moves[0], pokes[0].stats['sp'], targets[0], 'user', 0], [pokes[1],moves[1],pokes[1].stats['sp'], targets[1], 'user', 1], \
		[pokes[2],moves[2],pokes[2].stats['sp'], targets[2], 'opponent', 2], [pokes[3],moves[3],pokes[3].stats['sp'], targets[3], 'opponent', 3]]
	# First, the turn order is sorted by if any pokemon are switching (pursuit not accounted for, only losers use pursuit)
	switches = []
	for i in range(len(turnOrder)):
		if turnOrder[i][1] == 'switch':
			switches.append(turnOrder[i])

	# Next, we sort the remaining moves by priority
	nonSwitches = [turnOrder[i] for i in range(len(turnOrder)) if turnOrder[i][1] != 'switch']
	nonSwitches.sort(key = lambda x: x[1].priority, reverse=True)

	# Finally, we look at turn order based on pokemon speed. This is the only metric that is affected by trick room
	nonSwitches = SpeedSort(nonSwitches, field.trickRoom)

	# We update our turn order based on the 3 separate sorts we performed
	turnOrder = switches + nonSwitches

	# print(turnOrder[0][0].name.name, turnOrder[0][1].name, turnOrder[1][0].name.name, turnOrder[1][1].name, turnOrder[2][0].name.name, turnOrder[2][1].name, turnOrder[3][0].name.name, turnOrder[3][1].name)

	# Next, we sequentially take the actions
	for i in range(len(turnOrder)):
		attackerSide = turnOrder[i][4]
		target = turnOrder[i][3]
		if attackerSide == 'user':
			user = 0 if pokes[0].name.name == turnOrder[i][0].name.name else 1
		else:
			user = 2 if pokes[2].name.name == turnOrder[i][0].name.name else 3
		moveResult = result()
		for t in target:
			if t == 0 and repeat: # switching flag
				inTarget = target[1] - 5
				outMon = turnOrder[i][0]
				if inTarget <= 2:
					inMon = field.userSide.availablePokes[inTarget]
					field.userSide.availablePokes[inTarget] = turnOrder[i][0]
					userIndex = 0 if turnOrder[i][0].name.name == field.userSide.pokes[0].name.name else 1
					turnOrder[i][0] = inMon
					pokeIndex = 0 if pokes[0].name.name == outMon.name.name else 1
					pokes[pokeIndex] = inMon
					field.userSide.pokes[userIndex] = inMon
				else:
					inMon = field.opponentSide.availablePokes[inTarget-2]
					field.opponentSide.availablePokes[inTarget-2] = turnOrder[i][0]
					userIndex = 0 if turnOrder[i][0].name.name == field.opponentSide.pokes[0].name.name else 1
					pokeIndex = 2 if pokes[2].name.name == outMon.name.name else 3
					pokes[pokeIndex] = inMon
					turnOrder[i][0] = inMon
					field.opponentSide.pokes[userIndex] = inMon
				if repeat:
					pass
					# print(f'{attackerSide}\'s {outMon.name.name} switched with {inMon.name.name}')
				if t == 1 or t == 2:
					defenderSide = 'user'
				else:
					defenderSide = 'opponent'
				moveResult = damageCalc.TakeMove(inMon, attackerSide, outMon, defenderSide, turnOrder[i][1], field, target, moveResult)
				moveResult.user = user
				moveResult.target.append(t)
				moveResult.target.append(target[1])

			elif(t > 0 and t <= 4): # 1 <= target <= 4
				if t == 1 or t == 2:
					defenderSide = 'user'
				else:
					defenderSide = 'opponent'
				defender = pokes[t-1]
				if not (turnOrder[i][1].name == 'Sucker Punch' and moves[t-1].category == 'Status'):
					if repeat:
						pass
						# print(f'move {i+1}: {attackerSide}\'s {turnOrder[i][0].name.name} uses {turnOrder[i][1].name} against {defenderSide}\'s {defender.name.name}')
					moveResult = damageCalc.TakeMove(turnOrder[i][0], attackerSide, defender, defenderSide, turnOrder[i][1], field, t, moveResult)
				moveResult.user = user
				moveResult.target.append(t)
		moveResult.turnOrder = turnOrder
		actionVec.append(actionVector(moveResult))

	return actionVec

# bubblesort for remaining ties, needed to be done manually to also check for levels of priority
def SpeedSort(turns, trickRoom=False):
	sort = False
	while(not sort):
		sort = True
		if trickRoom:
			for i in range(len(turns)-1):
				if turns[i][1].priority == turns[i+1][1].priority and turns[i][2] > turns[i+1][2]:
					temp = turns[i]
					turns[i] = turns[i+1]
					turns[i+1] = temp
					sort = False
		else:
			for i in range(len(turns)-1):
				if turns[i][1].priority == turns[i+1][1].priority and turns[i][2] < turns[i+1][2]:
					temp = turns[i].copy()
					turns[i] = turns[i+1].copy()
					turns[i+1] = temp
					sort = False
	return turns

# Our dynamics function updates the state of our environment based on the actions taken.
# The envMode can either be 'simulation' or 'assistive'. Simulation means the results of the
# actions are not known beforehand; specifically, the stochastic actions (damage rolls, status chances, etc.)
# need to be simulated in the dynamics function. In comparison, in assistive mode the dynamics function will
# ask for any stochastic data and use that to both update the state and better understand the POMDP's unobserved states.
def ConvertFieldInfo(state, field):

	state[4][0] = field[0]
	state[4][1] = field[1]
	if field[2] and state[4][2] == False:
		state[4][2] = True
	elif field[2] and state[4][2] == True:
		state[4][2] = False
		state[4][3] = 5
	state[4][4] = field[4]
	state[4][5] = field[5]
	state[4][6] = field[6]
	state[4][7] = field[7]

	return state

def ConvertSideInfo(state, side, pos):
	if pos < 2:
		index = 5
	else:
		index = 6

	if state[index][0] == False and side[0] == True:
		state[index][0] == True

	if state[index][2] == False and side[2] == True:
		state[index][2] == True

	if state[index][4] == False and side[4] == True:
		state[index][4] == True

	if state[index][6] == False and side[6] == True:
		state[index][6] == True

	state[index][8] = side[8]
	state[index][9] = side[9]
	state[index][10] = side[10]
	state[index][11] = side[11]

	return state

def ResetConditions(field, state):
	field.userSide.isWideGuard = False
	field.userSide.isQuickGuard = False
	field.userSide.isHelpingHand = False
	field.opponentSide.isWideGuard = False
	field.opponentSide.isQuickGuard = False
	field.opponentSide.isHelpingHand = False
	for i in range(2):
		field.userSide.pokes[i].isFollowMe = False
		field.userSide.pokes[i].isProtected = False
		field.opponentSide.pokes[i].isFollowMe = False
		field.opponentSide.pokes[i].isProtected = False
	state = StateVector(field, field.userSide.pokes, field.opponentSide.pokes)
	return state

def Dynamics(state, field, pokes, moves, targets, availablePokes, envMode='simulation'):
	# To clarify: the length of the action vector is only at max 4, but each element is a large vector containing all the information of that move
	KOs = []
	for i in range(len(pokes)):
		action = TakeAction(field, pokes, moves, targets, availablePokes, False)
		fieldVec = action[i][2]
		userSideVec = action[i][3]
		opponentSideVec = action[i][4]
		if fieldVec[4]:
			field.isBeadsOfRuin = True
		if fieldVec[5]:
			field.isSwordOfRuin = True
		if fieldVec[6]:
			field.isTabletsOfRuin = True
		if fieldVec[7]:
			field.isVesselOfRuin = True
		if i < 2:
			if userSideVec[8]:
				field.userSide.isFriendGuard = True
		else:
			if opponentSideVec[8]:
				field.opponentSide.isFriendGuard = True


	for i in range(len(pokes)):
		if i == 0:
			action = TakeAction(field, pokes, moves, targets, availablePokes, True)
		else:
			action = TakeAction(field, pokes, moves, targets, availablePokes, False)
		userPos = action[i][0]
		targetPos = action[i][1]

		if len(targetPos) > 1:
			for t in targetPos:
				if t-1 in KOs:
					targetPos.remove(t)

		if targetPos[0] == 0:
			# inTarget = targetPos[1] - 5
			# if inTarget <= 2:
			# 	print('in before', field.userSide.availablePokes[inTarget])
			# 	print('out before', field.userSide.pokes[userPos])
			# 	# outMon = field.userSide.pokes[userPos]
			# 	inMon = field.userSide.availablePokes[inTarget]
			# 	field.userSide.availablePokes[inTarget] = field.userSide.pokes[userPos]
			# 	pokeIndex = 0 if pokes[0].name.name == field.userSide.pokes[userPos].name.name else 1
			# 	pokes[pokeIndex] = inMon
			# 	field.userSide.pokes[userPos] = inMon
			# 	print('in after', field.userSide.availablePokes[inTarget])
			# 	print('out after', field.userSide.pokes[userPos])
			# else:
			# 	outMon = field.opponentSide.pokes[userPos-2]
			# 	inMon = field.opponentSide.availablePokes[inTarget-2]
			# 	field.userSide.availablePokes[inTarget-2] = outMon
			# 	pokeIndex = 2 if pokes[2].name.name == outMon.name.name else 3
			# 	pokes[pokeIndex] = inMon
			# 	field.userSide.pokes[userPos-2] = inMon
			state = StateVector(field, field.userSide.pokes, field.opponentSide.pokes)

		elif len(targetPos) == 1:
			if targetPos[0]-1 in KOs:
				if targetPos[0] % 2 == 0:
					targetPos[0] -= 1
				else:
					targetPos[0] += 1
				if targetPos[0] not in KOs:
					if userPos < 2:
						attackerSide = 'user'
					else:
						attackerSide = 'opponent'
					if targetPos[0] <= 2:
						defenderSide = 'user'
					else:
						defenderSide = 'opponent'
					newResult = result()
					newResult = damageCalc.TakeMove(pokes[userPos], attackerSide, pokes[targetPos[0]-1], defenderSide, moves[userPos], field, targetPos[0], newResult)
					newResult.user = userPos
					newResult.target.append(targetPos[0])
					action[i] = actionVector(newResult)


		if userPos not in KOs and pokes[userPos].currHP > 0:
			state = ConvertFieldInfo(state, action[i][2])
			state = ConvertSideInfo(state, action[i][3], userPos)
			for t in targetPos:
				state = ConvertSideInfo(state, action[i][4], t)
			userOrder = [action[j][0] for j in range(4)]
			for j in range(4):
				inRangeHealth = min(state[j][2], max(0, state[j][14] - action[i][5+j][-1]))
				if inRangeHealth == 0 and state[j][14] == state[j][2] and state[j][15] == 1: # Focus band check
					inRangeHealth += 1
				if j == 0:
					pass
					# print(f'move {i}')
				# print(f'{pokes[j].name.name}\'s HP: {state[j][14]}; damage dealt: {state[j][14] - inRangeHealth}')
				state[j][14] = inRangeHealth
				#pokes[userPos].currHP = inRangeHealth
				fieldVec = action[j][2]
				if fieldVec[0] > 0:
					field.weather = field.weatherList[fieldVec[0]]
				if fieldVec[1] > 0:
					field.terrain = field.terrainList[fieldVec[1]]
				if fieldVec[2]:
					field.trickRoom = not field.trickRoom
					field.trickRoomTurns = 5
				if fieldVec[3] == 0:
					field.trickRoom = False
					field.trickRoomTurns = 5

				if j < 2:

					field.userSide.pokes[j].currHP = state[j][14]
					if len(action[i][9+j]) > 0:
						for k in range(len(action[i][9+j])):
							stat = action[i][9+j][k][0]
							stages = action[i][9+j][k][1]
							if envMode == 'Simulation' and action[i][9+j][k][2] <= 100:
								p = random.randint(0, 99)
								if action[i][9+j][k][2] > p:
									field.userSide.pokes[userOrder[j]].boosts[stat] += stages
							else:
								field.userSide.pokes[j].boosts[stat] += stages
					# print(field.userSide.pokes[j].boosts)

					if action[j][13]:
						field.userSide.pokes[userOrder[j]].isProtected = action[j][13]
					sideVec = action[j][3]
					if sideVec[0] and not field.userSide.isReflect:
						field.userSide.isReflect = True
						field.userSide.reflectTurns = 5
					elif field.userSide.reflectTurns == 0:
						field.userSide.isReflect = False

					if sideVec[2] and not field.userSide.isLightScreen:
						field.userSide.isLightScreen = True
						field.userSide.lightScreenTurns = 5
					elif field.userSide.lightScreenTurns == 0:
						field.userSide.isLightScreen = False

					if sideVec[4]:
						field.userSide.tailwind = True
						field.userSide.tailwindTurns = 4
					elif field.userSide.tailwindTurns == 0:
						field.userSide.tailwind = False
					if field.userSide.tailwind:
						field.userSide.tailwindTurns -= 1

					if sideVec[6] and not field.userSide.isAuroraVeil:
						field.userSide.isAuroraVeil = True
						field.userSide.auroraVeilTurns = 5
					elif field.userSide.auroraVeilTurns == 0:
						field.userSide.isAuroraVeil = False

					if sideVec[9]:
						field.userSide.isWideGuard = True
					if sideVec[10]:
						field.userSide.isQuickGuard = True
					if sideVec[11]:
						field.userSide.isHelpingHand = True

				else:
					field.opponentSide.pokes[j-2].currHP = state[j][14]


				if state[j][14] == 0 and j not in KOs:
					KOs.append(j)
					if pokes[j].ability == 'Beads Of Ruin':
						field.isBeadsOfRuin = False
					if pokes[j].ability == 'Sword Of Ruin':
						field.isSwordOfRuin = False
					if pokes[j].ability == 'Tablets Of Ruin':
						field.isTabletsOfRuin = False
					if pokes[j].ability == 'Vessel Of Ruin':
						field.isVesselOfRuin = False

		state = StateVector(field, field.userSide.pokes, field.opponentSide.pokes)

	for pos in KOs:
		if pos < 2:
			if envMode == 'simulation':
				if len(field.userSide.availablePokes) > 0:
					print(f'user\'s {pokes[pos].name.name} was KOed. Which pokemon will you switch with?')
					print(f'0: {field.userSide.availablePokes[0].name.name}')
					if len(field.userSide.availablePokes) == 2:
						print(f'1: {field.userSide.availablePokes[1].name.name}')
					newPoke = input()
					newPoke = int(newPoke)
					field.userSide.pokes[pos] = field.userSide.availablePokes[newPoke]
					pokes[pos] = field.userSide.availablePokes[newPoke]
					field.userSide.availablePokes.pop(newPoke)
			else:
				if len(field.userSide.availablePokes) > 0:
					field.userSide.pokes[pos] = field.userSide.availablePokes[0]
					pokes[pos] = field.userSide.availablePokes[0]
					field.userSide.availablePokes.pop(0)
					print('user switch')
		else:
			if len(field.opponentSide.availablePokes) > 0:
				field.opponentSide.pokes[pos-2] = field.opponentSide.availablePokes[0]
				pokes[pos] = field.opponentSide.availablePokes[0]
				field.opponentSide.availablePokes.pop(0)
				print('opponent switch')

	state = ResetConditions(field, state)
	state = StateVector(field, field.userSide.pokes, field.opponentSide.pokes)

	return state, field

def Reward(state, action, theta):
	userKOs = 0; oppKOs = 0
	switchReward = 0; switchCost = 0
	for i in range(2):
		if state[i][14] == 0:
			userKOs += 1
		if state[i+2][14] == 0:
			oppKOs += 1
		if len(action[i][1]) > 0:
			if action[i][1][0] == 0: # switching
				switchReward += 1
		if len(action[i+2][1]) > 0:
			if action[i+2][1][0] == 0:
				switchCost += 1

	KOReward = state[6][-1] + oppKOs
	KOCost = state[5][-1] + userKOs
	damageReward = 0; damageCost = 0
	speedReward = 1; speedCost = 1
	for i in range(4):
		userDamage = 0 if action[0][9] else action[i][5][-1] # Check protect for each mon
		allyDamage = 0 if action[1][9] else action[i][6][-1]
		opp1Damage = 0 if action[2][9] else action[i][7][-1]
		opp2Damage = 0 if action[3][9] else action[i][8][-1]

		damageReward += action[i][7][-1] + action[i][8][-1]
		damageCost += action[i][5][-1] + action[i][6][-1]
		for j in range(4):
			if len(action[i][9+j]) > 0:
				for k in range(len(action[i][9+j])):
					if action[i][9+j][k][0] == 5: # speed modifier
						if j < 2:
							speedReward *= action[i][9+j][k][1]*action[i][9+j][k][2] # number of stages multiplied by chance of boost occurring
						else:
							speedCost *= action[i][9+j][k][1]*action[i][9+j][k][2] # number of stages multiplied by chance of boost occurring
		if state[5][4]: # tailwind doubles speed, so double reward
			speedReward *= 2
		if state[6][4]:
			speedCost *= 2
	if damageReward > 0:
		damageReward = -1/damageReward
	else:
		damageReward = -2
	if damageCost > 0:
		damageCost = -1/damageCost
	else:
		damageCost = -2

	if speedReward > 0:
		speedReward = -1/speedReward
	else:
		speedReward = -2
	if speedCost > 0:
		speedCost = -1/speedCost
	else:
		speedCost = -2

	# print('KO Reward', KOReward)
	# print('KO Cost', KOCost)
	# print('Damage Reward', damageReward)
	# print('Damage Cost', damageCost)
	# print('Speed Reward', speedReward)
	# print('Speed Cost', speedCost)
	# print('Switch Reward', switchReward)
	# print('Switch Cost', switchCost)

	totalReward = (theta[0]*KOReward - theta[1]*KOCost) + (theta[2]*damageReward - theta[3]*damageCost) + \
		(theta[4]*speedReward - theta[5]*speedCost) + (theta[6]*switchReward - theta[7]*switchCost)

	beta = 1
	return np.exp(beta * totalReward)

def KOed(side):
	if len(side.availablePokes) == 0 and side.pokes[0].currHP == 0 and side.pokes[1].currHP == 0:
		return True
	return False
	
def demonstration():
	myField = field()
	userTeam, opponentTeam = CreateEnv()
	userPokes = random.sample(range(6), 4)
	myField.userSide.pokes[0] = userTeam[userPokes[0]]
	myField.userSide.pokes[1] = userTeam[userPokes[1]]
	myField.userSide.side = 'user'
	myField.userSide.availablePokes[0] = userTeam[userPokes[2]]
	myField.userSide.availablePokes[1] = userTeam[userPokes[3]]

	opponentPokes = random.sample(range(6), 4)
	myField.opponentSide.pokes[0] = opponentTeam[opponentPokes[0]]
	myField.opponentSide.pokes[1] = opponentTeam[opponentPokes[1]]
	myField.opponentSide.side = 'opponent'
	myField.opponentSide.availablePokes[0] = opponentTeam[opponentPokes[2]]
	myField.opponentSide.availablePokes[1] = opponentTeam[opponentPokes[3]]

	state = StateVector(myField, myField.userSide.pokes, myField.opponentSide.pokes)
	states = [state]
	actions = []

	pokes = myField.userSide.pokes + myField.opponentSide.pokes
	availablePokes = myField.userSide.availablePokes + myField.opponentSide.availablePokes
	print(f'In back mons: {myField.userSide.availablePokes[0].name.name}, {myField.userSide.availablePokes[1].name.name}')
	while not (KOed(myField.userSide) or KOed(myField.opponentSide)):
		print('User Pokemon #1: ')
		print(myField.userSide.pokes[0])
		print('User Pokemon #2: ')
		print(myField.userSide.pokes[1])
		print('Opponent Pokemon #1: ')
		print(myField.opponentSide.pokes[0])
		print('Opponent Pokemon #2: ')
		print(myField.opponentSide.pokes[1])

		print(myField.userSide.pokes[0].name.name, myField.userSide.pokes[0].currHP)
		print(myField.userSide.pokes[1].name.name, myField.userSide.pokes[1].currHP)
		print(myField.opponentSide.pokes[0].name.name, myField.opponentSide.pokes[0].currHP)
		print(myField.opponentSide.pokes[1].name.name, myField.opponentSide.pokes[1].currHP)
		moves = []
		targets = []
		for i in range(len(myField.userSide.pokes)):
			move = input('Which move will you take? ')
			target = input('Who are you targeting? ')
			target = target.split(',')
			target = [int(target[i].strip()) for i in range(len(target))]
			if move == 'switch':
				moves.append(move)
			else:
				moves.append(database.movesDict[move])
			targets.append(target)

		for i in range(len(myField.opponentSide.pokes)):
			ally = myField.opponentSide.pokes[1] if i == 0 else myField.opponentSide.pokes[0]
			move, target = maxDamageAI(myField.opponentSide.pokes[i], ally, myField.userSide, myField)
			moves.append(move)
			targets.append(target)

		action = TakeAction(myField, pokes, moves, targets, availablePokes, False)
		actions.append(str(action))

		state, myField = Dynamics(state, myField, pokes, moves, targets, availablePokes)
		states.append(str(state))
	if KOed(myField.opponentSide):
		print('you won!')
	else:
		print('you lost!')
	return states, actions

def Step(state, field, pokes, moves, targets, availablePokes):
	theta = pickle.load(open('IRLWeights.pkl', 'rb'))
	action = TakeAction(field, pokes, moves, targets, availablePokes, True)
	next_state = Dynamics(state, field, pokes, moves, targets, availablePokes, envMode='RL Learning')[0]
	reward = Reward(state, action, theta)
	dones = 1 if KOed(field.userSide) or KOed(field.opponentSide) else 0
	return action, next_state, reward, dones


