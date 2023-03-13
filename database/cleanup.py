"""
This script is used to fix formatting issues in the data files.
The fixed file is output under a temp name to prevent overwriting of
data and to check accuracy before replacing.

"""


inputFile = open("data/species.txt", "r")
outputFile = open("data/test.txt", "w")
for line in inputFile:
	line = line.strip()
	if len(line) > 0:
		if ord(line[0]) >= 65 and ord(line[0]) <= 90:
			endIndex = line.find(':')
			tempStr = f'\'{line[0:endIndex]}\'{line[endIndex:]}\n'
			outputFile.write(tempStr)
		else:
			tempStr = f'{line}\n'
			outputFile.write(tempStr)
inputFile.close()
outputFile.close()