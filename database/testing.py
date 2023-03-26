import re

files = open("database\statistics.txt", "r",encoding="utf8")
abilitiedata = False
itemdata = False
spreadsdata = False
movedata = False
AbilityDict = {}
SpreadDict = {}
ItemDict = {}
MoveDict = {}

for line in files:
    line = line.strip()
    # print(line)
    Abilities = line.find('Abilities')
    Items = line.find('Items')
    Spreads = line.find('Spreads')
    Moves = line.find('Moves')
    Teammates = line.find('Teammates')

    if Abilities != -1:
        abilitiedata = True
        itemdata = False
        spreadsdata = False
        movedata = False
    if Items != -1:
        abilitiedata = False
        itemdata = True
        spreadsdata = False
        movedata = False
    if Spreads != -1:
        abilitiedata = False
        itemdata = False
        spreadsdata = True
        movedata = False
    if Moves != -1:
        abilitiedata = False
        itemdata = False
        spreadsdata = False
        movedata = True
    if Teammates != -1:
        abilitiedata = False
        itemdata = False
        spreadsdata = False
        movedata = False

    # print(line,"Ability check",abilitiedata)
    if abilitiedata == True:
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
            AbilityDict[key] = item
            # print(AbilityDict)


    if itemdata == True:
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
            ItemDict[key] = item
            # print(ItemDict)

    if spreadsdata == True:
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
            SpreadDict[key] = item
            print(SpreadDict)


    if movedata == True:
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
            MoveDict[key] = item
            # print(MoveDict)
    