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

class calc:
	database = database()
	database.addMoves()
	database.addTypes()
	database.addSpecies()
	database.addNatures()


