from side import side

class field:
	def __init__(self):
		self.weather = 'None'
		self.weatherList = ['None', 'Sand', 'Sun', 'Rain', 'Snow']
		self.terrain = 'None'
		self.terrainList = ['None', 'Electric', 'Grassy', 'Psychic', 'Misty']
		self.gravity = False
		self.trickRoom = False
		self.trickRoomTurns = 5
		self.isBeadsOfRuin = False
		self.isSwordOfRuin = False
		self.isTabletsOfRuin = False
		self.isVesselOfRuin = False
		self.userSide = side()
		self.opponentSide = side()
		self.isGhostRevealed = False