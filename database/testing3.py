from species import species
from testing2 import statistics

speciesDic = {}
speciesFile = open("database/species.txt", "r",encoding="utf8")
for line in speciesFile:
	line = line.strip()
	if len(line) > 0:
		if line[0] == '\'':
			colonIndex = line.find(':')
			newSpecies = species()
			newSpecies.name = line[1:colonIndex-1]
			if newSpecies.name in speciesDic.keys():
				newSpecies = speciesDic[newSpecies.name]
			if line.find('}') != -1:
				newSpecies.addData(line)
			else:
				while line[0] != '}':
					newSpecies.addData(line)
					line = next(speciesFile)
			
			speciesDic[newSpecies.name] = newSpecies
speciesFile.close()

nameList = list(speciesDic.keys())
# print(name)

# Initialize the data
statsDic = {}
nameFlag = False # set the name flag to True so it can extract the first pokemon's data
statFile = open('database/statistics.txt','r',encoding='utf8')
# Read the data from the file
newStates = statistics()
for line in statFile:
	line = line.strip()
	# print(line)
	if any(name in line for name in nameList) and '%' not in line:
		nameFlag = True
	else:
		nameFlag = False
	# print(line,'     ',nameFlag)
	if len(line) > 0:
		if nameFlag == True:
			newStates = statistics()
			newStates.addData(line)	
			startIndex = line.find('|')
			endIndex = line.find('+')
			tempLine = line[startIndex+1:endIndex].strip()
			newStates.name = tempLine
			# print(newStates)
		else:
			newStates.addData(line)
		statsDic[newStates.name ] = newStates
print(statsDic)

	

statFile.close

# print(newStates)
	


		