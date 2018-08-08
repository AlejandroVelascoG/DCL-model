# Code for the model of division of cognitive labor
# with focal pahts.
# Edgar Andrade, Miguel Valencia, Juan Camilo Hoyos
# 2018

import focalPaths as fp
from random import uniform

# ------------------------------------------
# Parameters
# ------------------------------------------
# Define model parameters
p = 0.5 # probability of there being a unicorn
Pl = 2 # number of players
Num_Loc = 8 # number of locations (squares in a row in the grid)
SIZE = [1]*64
numIter = 20
Tolerance_Global = [30, 30, 30, 30]
Stubornness_Global = [3, 3, 3, 3]
# Threshold_Global = [0.5, 0.55, 0.60, 0.65]
Threshold_Global = [0.65, 0.7, 0.75, 0.8]
Exp_Global = Threshold_Global

rotulo = "Threshold behavior"

# ------------------------------------------
# Here begins the action
# ------------------------------------------

# Open files to save data
f = open("raw_sim.csv", 'w')

# Initialize files with headers
cols = 'Exp,Dyad,Round,Player,Answer,Time,'
for i in range(0, Num_Loc):
	for j in range(0, Num_Loc):
		cols += 'a' + str(i+1) + str(j+1) + ','
for i in range(0, Num_Loc):
	for j in range(0, Num_Loc):
		cols += 'b' + str(i+1) + str(j+1) + ','
cols += 'Score,Joint,Is_there,where_x,where_y\n'
f.write(cols)


n = len(Exp_Global)

for i in range(n):
    print "Corriendo con parametro " + rotulo + " = " + str(Exp_Global[i])

    for j in range(45):
        fp.experimento(Pl, \
                       SIZE, \
                       Num_Loc, \
                       numIter, \
                       p, \
                       Tolerance_Global[i], \
                       Stubornness_Global[i], \
                       Threshold_Global[i], \
                       Exp_Global[i], \
                       f)

f.close()
print "Experiment done!"

# fp.get_measures()
