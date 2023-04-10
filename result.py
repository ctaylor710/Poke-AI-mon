from database.database import database
from field import field
from side import side
'''
This class is designed to provide as much information as possible about the next state of our environment.

'''

class result:
	def __init__(self):
		self.attackerSide = side()
		self.defenderSide = side()
		self.field = field()
		self.opponentDamage = []
		self.selfDamage = 0
		self.opponentStatChanges = [] # each item should be a tuple of the form ('stat name', #stages, % chance)
		self.selfStatChanges = []
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
