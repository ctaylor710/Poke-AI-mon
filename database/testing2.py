# TODO 1. Convert everything into a class
class statistics:
    
    def __int__(self):
        self.name='None'
        self.AbilitiesDict = {}
        self.ItemsDict = {}
        self.MovesDict = {}
        self.NaturesDict = {}
        self.SpreadDict = {}
        # Initialize all the flags to False
        self.abilitiesdata = False
        self.itemdata = False
        self.spreadsdata = False
        self.movedata = False

    def addData(self, line):
        Abilities = line.find('Abilities')
        if Abilities != -1:
            self.abilitiesdata = True
            self.itemdata = False
            self.spreadsdata = False
            self.movedata = False

        Items = line.find('Items')
        if Items != -1:
            self.abilitiesdata = False
            self.itemdata = True
            self.spreadsdata = False
            self.movedata = False  
    
        Spreads = line.find('Spreads')
        if Spreads != -1:
            self.abilitiesdata = False
            self.itemdata = False
            self.spreadsdata = True
            self.movedata = False
        
        Moves = line.find('Moves')
        if Moves != -1:
            self.abilitiesdata = False
            self.itemdata = False
            self.spreadsdata = False
            self.movedata = True
        # Teammates is a data we don't need, so I used to reset all the flag back to false
        Teammates = line.find('Teammates')
        if Teammates != -1:
            self.abilitiesdata = False
            self.itemdata = False
            self.spreadsdata = False
            self.movedata = False

        
        if self.abilitiesdata == True:
            startIndex = line.find('|')
            endIndex = line.find('+')
            tempLine = line[startIndex+1:endIndex].strip()
            if any(chr.isdigit() for chr in tempLine) == True:
                tempLine = tempLine.strip("%")
                tempLine = tempLine.split(" ")
                tempLine = [x for x in tempLine if x != '']
                key = ""
                item = 0
                for idx in range(len(tempLine)):
                    valuecheck = '.'
                    if valuecheck not in tempLine[idx]:
                        # it's the name
                        if idx != 0:
                            tempLine[idx] = " " + tempLine[idx]
                            key += tempLine[idx]
                        else:
                            key += tempLine[idx]
                    else:
                        # it's the probability
                        item = round(float(tempLine[idx])/100,5)
                self.AbilitiesDict[key] = item
                # print(AbilityDict)

        if self.itemdata == True:
            startIndex = line.find('|')
            endIndex = line.find('+')
            tempLine = line[startIndex+1:endIndex].strip()
            if any(chr.isdigit() for chr in tempLine) == True:
                tempLine = tempLine.strip("%")
                tempLine = tempLine.split(" ")
                tempLine = [x for x in tempLine if x != '']
                key = ""
                item = 0
                for idx in range(len(tempLine)):
                    valuecheck = '.'
                    if idx == 0:
                        key += tempLine[idx]
                    elif valuecheck not in tempLine[idx] and idx != 0:
                        # it's the name
                        tempLine[idx] = " " + tempLine[idx]
                        key += tempLine[idx]  
                    else:
                        # it's the probability
                        item = round(float(tempLine[idx])/100,5)
                self.ItemsDict[key] = item
                # print(ItemDict)

        if self.spreadsdata == True:
            startIndex = line.find('|')
            endIndex = line.find('+')
            tempLine = line[startIndex+1:endIndex].strip()
            if any(chr.isdigit() for chr in tempLine) == True:
                tempLine = tempLine.strip("%")
                tempLine = tempLine.split(" ")
                tempLine = [x for x in tempLine if x != '']
                key = ""
                item = 0
                for idx in range(len(tempLine)):
                    valuecheck = '.'
                    if idx == 0:
                        key += tempLine[idx]
                    elif valuecheck not in tempLine[idx] and idx != 0:
                        # it's the name
                        tempLine[idx] = " " + tempLine[idx]
                        key += tempLine[idx]  
                    else:
                        # it's the probability
                        item = round(float(tempLine[idx])/100,5)
                self.SpreadDict[key] = item

        if self.movedata == True:
            startIndex = line.find('|')
            endIndex = line.find('+')
            tempLine = line[startIndex+1:endIndex].strip()
            if any(chr.isdigit() for chr in tempLine) == True:
                tempLine = tempLine.strip("%")
                tempLine = tempLine.split(" ")
                tempLine = [x for x in tempLine if x != '']
                # figure out a way to combile the splited line into a Dictionary
                key = ""
                item = 0
                for idx in range(len(tempLine)):
                    valuecheck = '.'
                    if idx == 0:
                        key += tempLine[idx]
                    elif valuecheck not in tempLine[idx] and idx != 0:
                        # it's the name
                        tempLine[idx] = " " + tempLine[idx]
                        key += tempLine[idx]  
                    else:
                        # it's the probability
                        item = round(float(tempLine[idx])/100,5)
                self.MovesDict [key] = item

    def __str__(self):
        str=f'Species: {self.name}\nAbilities: {self.AbilitiesDict}\nItems: {self.ItemsDict}\nMoves: {self.MovesDict}\nNatures: {self.NaturesDict}\n'
        str+=f'Spreads: {self.SpreadDict}\n'
        return str

# TODO 2. Initiate the data
statisticsDict = {}
namedata = True # This set up a flag to make sure the data taken are the name of pokemon
statisticsFile = open("database/statistics.txt","r",encoding="utf8")

for line in statisticsFile:
    line = line.strip()
    if len(line) > 0:
        # Get Index, Raw is where the name ends, and check is where the next name started
        Raw = line.find('Raw count')
        check = line.find('Checks and Counters')
        # Set the namedata flag to off if it is at the raw count
        if Raw != -1:
            namedata = False
        if check != -1:
            namedata = True

        newStats = statistics()
        print(newStats.abilitiesdata)

        if namedata == True:
            # Get Index
            startIndex = line.find('|')
            endIndex = line.find('+')
            tempLine = line[startIndex+1:endIndex].strip()

            # Get rid of the 'Check and Counters' and empty spaces
            if tempLine != 'Checks and Counters' and len(tempLine) > 0:
                newStats.name = tempLine

                
        # else:
        #     newStats.addData(line)
        #     statisticsDict[newStats.name] = newStats
            

statisticsFile.close()

# print(statisticsDict)
            