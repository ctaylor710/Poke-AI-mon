from pokemon import pokemon

class side:
	def __init__(self):
		self.side = 'user'
		self.pokes = [pokemon(), pokemon()]
		self.availablePokes = [pokemon(), pokemon()]
		self.spikes = 0
		self.toxicSpikes = 0
		self.stealthRock = False
		self.isReflect = False
		self.isLightScreen = False
		self.tailwind = False
		self.isAuroraVeil = False
		self.friendGuard = False
		self.isProtected = False
		self.isWideGuard = False
		self.isQuickGuard = False
		self.isForesight = False
		self.isHelpingHand = False