# Get measures from simulation
# Measures are: accumulated score, normalized score, number of tiles visited,
# consistency, total of tiles visited dyad, difference in consistency, DLIndex,
# distance to closest focal path, and fairness.

print "loading packages..."
import numpy as np
import pandas as pd

# Opens the file with data from DCL experiment into a Pandas DataFrame
print "Reading data..."

data_archivo = 'raw_sim.csv'

data = pd.read_csv(data_archivo, index_col=False)
print "Data read!"

# --------------------------------------------------
# Parameters
# --------------------------------------------------
Num_Loc = 8

# --------------------------------------------------
# Obtaining measures from players' performance
# --------------------------------------------------
# Find the accumulated score
print "Finding accumulated score..."
data['Ac_Score'] = data.sort_values(['Dyad','Player']).groupby('Player')['Score'].cumsum()
# print data

# --------------------------------------------------
# Working only with trials with "Unicorn_Absent"
# --------------------------------------------------
data = pd.DataFrame(data.groupby('Is_there').get_group('Unicorn_Absent')).reset_index()
# data = pd.DataFrame(data.groupby('Is_there').get_group('Unicorn_Absent'))


# --------------------------------------------------
# Continue obtaining measures
# --------------------------------------------------
Dyads = data.Dyad.unique()

# Find the normalized score
max_score = 32
min_score = -64 - 64
print "Finding normalized score..."
data['Norm_Score'] = (data['Score'] - min_score) / (max_score - min_score)
# print data

# Find the number of tiles visited per round per player
cols = ['a' + str(i+1) + str(j+1) for i in range(0, Num_Loc) for j in range(0, Num_Loc)]
data['Size_visited'] = data[cols].sum(axis=1)
# print data[:10]
cols2 = ['a' + str(i + 1) + str(j + 1) for i in range(0, Num_Loc) for j in range(0, Num_Loc)]
dts = []
cols22 = ['Inters-' + c for c in cols2]
# print data[cols22]
cols222 = ['Unions-' + c for c in cols2]
# print data[cols222]
for key, grp in data[cols2 + ['Player']].groupby(['Player']):
	# print "Processing player: ", key
	aux1 = pd.DataFrame(np.floor(grp[cols2].rolling(2).mean()))
	aux2 = pd.DataFrame(np.ceil(grp[cols2].rolling(2).mean()))
	AAAA = pd.concat([aux1, aux2], axis=1)
	AAAA.columns = cols22 + cols222
	AAAA['Inters'] = AAAA[cols22].sum(axis=1)
	AAAA['Unions'] = AAAA[cols222].sum(axis=1)
	AAAA['Consistency'] = AAAA['Inters']/AAAA['Unions']
	# print AAAA['Consistency']
	dts.append(AAAA['Consistency'])

# rerer = pd.merge(dts[0], dts[1], left_index=True, right_index=True, how='outer')
rerer = pd.concat(dts, axis=1)
# print rerer.columns.values
columnas = []
nombres = list(rerer.columns.values)
# print nombres
for i in range(len(nombres)):
	columnas.append(str(i))
# print columnas
rerer.columns = columnas
# print rerer.columns.values
# print rerer.shape
rerer['Consistency'] = rerer['0']
for i in range(1, len(nombres)):
	rerer['Consistency'] = rerer['Consistency'].combine_first(rerer[str(i)])

data['Consistency'] = rerer['Consistency']
data['Consistency'] = data['Consistency'].fillna(1)
# data['Consistency'] = data['Consistency'].fillna(0)
# print data


# Find distance between players' strategies ----
print "Finding distance between players' strategies..."
# Find the squares visited by both players ----
cols = ['Dyad','Player','Size_visited', 'Consistency']
cols += ['a' + str(i+1) + str(j+1) for i in range(0, Num_Loc) for j in range(0, Num_Loc)]
Grps_Dyad = data[cols].groupby(['Dyad'])
total = []
dli = []
dif_cons = []
for d in Dyads:
	grp = Grps_Dyad.get_group(d)
	Players = grp.Player.unique()
	# print "The players in dyad " + str(d) + " are: " + str(Players)
	Grp_player = grp.groupby(['Player'])
	aux1 = pd.DataFrame(Grp_player.get_group(Players[0])).reset_index()
	aux2 = pd.DataFrame(Grp_player.get_group(Players[1])).reset_index()
	# print aux1['a11']
	# print aux2['a11']
	# a = [np.where(aux1['a' + str(i + 1) + str(j + 1)] + aux2['a' + str(i + 1) + str(j + 1)] >= 1, 1, 0) for i in range(0, Num_Loc) for j in range(0, Num_Loc)]
	a = [np.where(aux1['a' + str(i + 1) + str(j + 1)] + aux2['a' + str(i + 1) + str(j + 1)] >= 1, 1, 0) for i in range(0, Num_Loc) for j in range(0, Num_Loc)]
	aux3 = sum(a)
	# Finding difference between consistencies
	# print "La consistencia de uno es " + str(aux1['Consistency'])
	# print "La consistencia de otro es " + str(aux2['Consistency'])
	aux4 = np.absolute(aux1['Consistency'] - aux2['Consistency'])
	# print "La dif consistencia es " + str(aux4)
	# print "El total de locaciones visitas por los dos jugadores en" + \
	"la pareja " + str(d) + " es: " + str(aux3)
	for j in aux3:
		# print "j: " + str(j) + " comp. dist.: " + str(1-float(j)/Num_Loc)
		total.append(j)
		total.append(j)
		# preparing to add dif_cons
	for j in aux4:
		dif_cons.append(j)
		dif_cons.append(j)

# print str(len(data)) + " " + str(len(total))
data['Total_visited_dyad'] = total
# #print data[:3]
data['Dif_consist'] = dif_cons
# print data['Dif_consist'][:3]

# Division of labor Index (Goldstone)
data['DLIndex'] = (data['Total_visited_dyad'] - data['Joint'])/(Num_Loc*Num_Loc)
data['DLIndex_Mean'] = data['DLIndex'].groupby(data['Dyad']).transform('mean')


# Find fairness between players' split of the grid ----
print "Finding fairness..."
# Find the squares visited by both players ----
cols = ['Dyad','Player','Size_visited']
Grps_Dyad = data[cols].groupby(['Dyad'])
Dyads = data.Dyad.unique()
data['Fairness'] = np.nan
print "Data primeros 3\n", data[:3]
for d in Dyads:
	grp = Grps_Dyad.get_group(d)
	Players = grp.Player.unique()
	# print "The players in dyad " + str(d) + " are: " + str(Players)
	Grp_player = grp.groupby(['Player'])
	aux1 = pd.DataFrame(Grp_player['Size_visited'].get_group(Players[0]))
	aux2 = pd.DataFrame(Grp_player['Size_visited'].get_group(Players[1]))
	# print "Here we find the fairness"
	aux1['Size_visited'] = aux1.Size_visited.astype(float)
	# print "aux1\n", aux1['Size_visited'][:3]
	# print "aux2\n", aux2['Size_visited'][:3]
	se = pd.Series(list(aux2['Size_visited'])) # capturo los valores del otro jugador
	aux1['Fairness'] = 1 - np.absolute(aux1['Size_visited'] - se.values)/(Num_Loc * Num_Loc)
	# print "aux1\n", aux1
	se = pd.Series(list(aux1['Fairness'])) # duplico los valores de fairnes del primer jugador
	aux2['Fairness'] = se.values # y se los pego al segundo
	# print "aux2\n", aux2
	fairness = pd.concat([aux1, aux2], axis=1)
	columnas = ['a', 'f1', 'b', 'f2']
	fairness.columns = columnas
	# print "fairness primeros 3\n", fairness[:3]
	fairness['f1'] = fairness['f1'].combine_first(fairness['f2'])
	# print "fairness primeros 3\n", fairness[:3]
	# print "fairness 60 a 63", fairness[60:63]
	# print fairness.shape
	data['Fairness'] = data['Fairness'].combine_first(fairness['f1'])
	# print "Data\n", data['Fairness']

data.to_csv('sim_dat.csv', index=False)
print "Results saved to sim_dat.csv"

print "Done!"
