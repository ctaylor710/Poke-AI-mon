def statTable():
	return {'hp':0, 'at':1, 'df':2, 'sa':3, 'sd':4, 'sp':5}

stat = 0

statTableCopy = statTable()
statTableCopy = {i: k for k, i in statTableCopy.items()}
statName = statTableCopy.get(stat)
print(statName)