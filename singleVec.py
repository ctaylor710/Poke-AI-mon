
# TODO 1.2 create a function that do the above things
def strip(r):
    list_temp = []
    isList = False # A flag to check the list after stripping contains any list in side
    for idx in range(len(r)):
        temp = r[idx]
        if type(temp) == list:
            list_temp.extend(temp)  # If the element is a list, extend it to the temp list
        else:
            list_temp.append(temp)  # If it is a number or booling, append it to the temp list
    for idy in range(len(list_temp)):
        temp = list_temp[idy]
        if type(temp) == list:
            isList = True  
    return list_temp, isList

def bo2int(r):
    list_temp = r.copy()
    for idx in range(len(r)):
        temp = r[idx]
        if temp == True:
            list_temp[idx] = 1
        elif temp == False:
            list_temp[idx] = 0
    return list_temp

def rework(r):
    r, isList = strip(r)
    while isList:
        r, isList = strip(r)
    r = bo2int(r)
    return r
