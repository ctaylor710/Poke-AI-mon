class statistics:
    def __int__(self):
        self.name = 'None'
        self.AbilitiesDict  = {}
        self.ItemsDict  = {}
        self.MovesDict  = {}
        self.NaturesDict  = {}
        self.SpreadDict  = {}
        # Initialize all the flags to False
        self.abilitiedata = False
        self.itemdata = False
        self.spreadsdata = False
        self.movedata = False

    def addData(self, line):
        # tooke out empty space at the start and end of the line
        line = line.strip()
        # Find the location of the words and set a flag on it
        Abilities = line.find('Abilities')
        if Abilities != -1:
            self.abilitiedata = True
            self.itemdata = False
            self.spreadsdata = False
            self.movedata = False

        Items = line.find('Items')
        if Items != -1:
            self.abilitiedata = False
            self.itemdata = True
            self.spreadsdata = False
            self.movedata = False
        
    
        Spreads = line.find('Spreads')
        if Spreads != -1:
            self.abilitiedata = False
            self.itemdata = False
            self.spreadsdata = True
            self.movedata = False
        
        Moves = line.find('Moves')
        if Moves != -1:
            self.abilitiedata = False
            self.itemdata = False
            self.spreadsdata = False
            self.movedata = True
        # Teammates is a data we don't need, so I used to reset all the flag back to false
        Teammates = line.find('Teammates')
        if Teammates != -1:
            self.abilitiedata = False
            self.itemdata = False
            self.spreadsdata = False
            self.movedata = False

        
        if self.abilitiedata == True:
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