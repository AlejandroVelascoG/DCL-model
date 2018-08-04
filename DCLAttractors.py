print "loading packages..."
import RandomPath as rp
import ExploreGrid as eg

# ------------------------------------------
# Parameters
# ------------------------------------------
# Define model parameters
# p = 0.5 # probability of there being a unicorn
# Pl = 2 # number of players
# Num_Loc = 8 # number of locations (squares in a row in the grid)

# ------------------------------------------
# Here begins the action
# ------------------------------------------
# Creates the players
# Requires import ExploreGrid as eg
# Players = []
# for k in range(0, Pl):
# 	Players.append(eg.player(False, "", [], [], 0, False, int(uniform(0, 1000000))))
#
# # Open files to save data
# f = open("raw_sim.csv", 'w')
#
# # Initialize files with headers
# cols = 'Dyad,Round,Player,Answer,Time,'
# for i in range(0, Num_Loc):
# 	for j in range(0, Num_Loc):
# 		cols += 'a' + str(i+1) + str(j+1) + ','
# for i in range(0, Num_Loc):
# 	for j in range(0, Num_Loc):
# 		cols += 'b' + str(i+1) + str(j+1) + ','
# cols += 'Score,Joint,Is_there,where_x,where_y\n'
# f.write(cols)

eg.comprobarExploreGrid()



# f.close()
