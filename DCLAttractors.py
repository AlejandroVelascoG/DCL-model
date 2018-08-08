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
numIter = 60
Tolerance = 30
Stubornness = 3
Threshold = 0.1
# ------------------------------------------
# Here begins the action
# ------------------------------------------

# Creates the players
Players = []
for k in range(0, Pl):
	Players.append(fp.player(\
                             False,\
                             "",\
                             fp.RandomPath(SIZE),\
                             int(uniform(0, 1000)), \
                             [],\
                             False, \
                             0\
                             )\
                    )

# Open files to save data
f = open("raw_sim.csv", 'w')

# Initialize files with headers
cols = 'Dyad,Round,Player,Answer,Time,'
for i in range(0, Num_Loc):
	for j in range(0, Num_Loc):
		cols += 'a' + str(i+1) + str(j+1) + ','
for i in range(0, Num_Loc):
	for j in range(0, Num_Loc):
		cols += 'b' + str(i+1) + str(j+1) + ','
cols += 'Score,Joint,Is_there,where_x,where_y\n'
f.write(cols)

countB = 0 # Initializes couter for Stubornness

for i in range(numIter):

    regions = fp.ExploreGrid(p, Num_Loc, Players,f, i)

    for k in range(len(Players)):

        Minimo, camino = fp.find_min_distance_2_Focal(Players[k].path, Num_Loc)

        if Minimo == 0:
            if (Players[k].score < Tolerance):
                countB += 1
                if countB > Stubornness:
                    Players[k].path = fp.RandomPath(SIZE)

        else:
            Path = fp.analyze(regions[k], Threshold, SIZE, Num_Loc)
            Minimo, camino = fp.find_min_distance_2_Focal(Path, Num_Loc)
            if Minimo == 0:
                Players[k].path = camino
                countB = 0

f.close()
