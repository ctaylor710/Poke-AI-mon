from side import side

class field:
	def __init__(self):
		self.weather = 'None'
		self.weatherList = ['Sand', 'Sun', 'Rain', 'Snow']
		self.terrain = 'None'
		self.terrainList = ['Electric', 'Grassy', 'Psychic', 'Misty']
		self.gravity = False
		self.trickRoom = False
		self.beadsOfRuin = False
		self.swordOfRuin = False
		self.tabletsOfRuin = False
		self.vesselOfRuin = False
		self.userSide = side()
		self.opponentSide = side()
		self.isGhostRevealed = False