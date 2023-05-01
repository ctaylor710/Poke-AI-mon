from database.database import database
from field import field
from side import side
from pokemon import pokemon
'''
This class is designed to provide as much information as possible about the next state of our environment.

'''

class result:
	def __init__(self):
		self.attacker = pokemon()
		self.defender = pokemon()
		self.attackerSide = side()
		self.defenderSide = side()
		self.field = field()
		self.opponentDamage = [0] * 16
		self.opponent2Damage = [0] * 16
		self.allyDamage = [0] * 16
		self.selfDamage = 0
		self.user = 0
		self.target = []
		self.opponentStatChanges = [] # each item should be a tuple of the form ('stat name', #stages, % chance)
		self.selfStatChanges = []
		self.allyStatChanges = []
		self.opponent2StatChanges = []
		self.protects = False
		self.flinch = 0 # value from 0 to 100 representing flinch chance
		self.traps = False
		self.burn = 0
		self.freeze = 0
		self.paralysis = 0
		self.poison = 0
		self.toxic = 0
		self.sleep = 0
		self.confusion = 0
		self.preventsSound = 0
		self.turnOrder = []