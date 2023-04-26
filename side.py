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
		self.reflectTurns = 5
		self.isLightScreen = False
		self.lightScreenTurns = 5
		self.tailwind = False
		self.tailwindTurns = 4
		self.isAuroraVeil = False
		self.auroraVeilTurns = 5
		self.friendGuard = False
		self.isWideGuard = False
		self.isQuickGuard = False
		self.isForesight = False
		self.isHelpingHand = False