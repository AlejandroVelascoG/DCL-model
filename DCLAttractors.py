print "loading packages..."
import RandomPath as rp
import ExploreGrid as eg
import Analyze as al

# ------------------------------------------
# Functions
# ------------------------------------------
def set_distance(l1, l2):
    # Finds the distance between lists l1 and l2
    # Lists l1 and l2 must contain only 0 and 1

    intersect = np.sum([np.where(l1[i] + l2[i] > 1, 1, 0) for i in range(0, Num_Loc * Num_Loc)])
    # print "Intersection: " + str(intersect)
    uni = np.sum([np.where(l1[i] + l2[i] > 0, 1, 0) for i in range(0, Num_Loc * Num_Loc)])
    # print "Union: " + str(uni)
    if uni == 0:
        return 0
    else:
        return 1 - (float(intersect)/uni)

def find_min_distance_2_Focal(path):
    '''
    Finds the minimum distance from a path to a focal path

    Input: path
    Output: minimum distance to a focal path,
            closest focal path
    '''

    print "Finding distances to focal paths..."

    size = Num_Loc * Num_Loc
    half_size = Num_Loc * Num_Loc / 2
    half_Num_Loc = Num_Loc / 2

    # First pair of complementary paths -- UD
    UP = [1] * half_size + [0] * half_size
    DOWN = [1 - i for i in UP]
    # Second pair of complementary paths -- LR
    RIGHT = []
    for i in range(0, Num_Loc):
        RIGHT += [0] * half_Num_Loc + [1] * half_Num_Loc

    LEFT = [1 - i for i in RIGHT]
    # Third pair of complementary paths -- AN
    ALL = [1] * size
    NOTHING = [0] * size
    # Fourth pair of complementary paths -- IO
    IN = []
    for i in range(Num_Loc):
        IN += [0] + [1] * (Num_Loc - 2) + [0]

    OUT = [1 - i for i in IN]

    # print "Finding distances to each focal path..."
    D_2_UP = set_distance(path, UP)
    D_2_DOWN = set_distance(path, DOWN)
    D_2_LEFT = set_distance(path, LEFT)
    D_2_RIGHT = set_distance(path, RIGHT)
    D_2_ALL = set_distance(path, ALL)
    D_2_NOTHING = set_distance(path, NOTHING)
    D_2_IN = set_distance(path, IN)
    D_2_OUT = set_distance(path, OUT)
    # print "D_2_UP: " + str(D_2_UP)
    # print "D_2_DOWN: " + str(D_2_DOWN)
    # print "D_2_LEFT: " + str(D_2_LEFT)
    # print "D_2_RIGHT: " + str(D_2_RIGHT)
    # print "D_2_ALL: " + str(D_2_ALL)
    # print "D_2_NOTHING: " + str(D_2_NOTHING)
    # print "D_2_IN: " + str(D_2_IN)
    # print "D_2_OUT: " + str(D_2_OUT)

    distances = {}

    distances[D_2_UP] = UP
    distances[D_2_DOWN] = DOWN
    distances[D_2_LEFT] = LEFT
    distances[D_2_RIGHT] = RIGHT
    distances[D_2_ALL] = ALL
    distances[D_2_NOTHING] = NOTHING
    distances[D_2_IN] = IN
    distances[D_2_OUT] = OUT

    minimo = min([\
                D_2_UP, D_2_DOWN, \
                D_2_LEFT, D_2_RIGHT, \
                D_2_ALL, D_2_NOTHING, \
                D_2_IN, D_2_OUT, \
                ])

    return minimo, distances[minimo]

# ------------------------------------------
# Parameters
# ------------------------------------------
# Define model parameters
p = 0.5 # probability of there being a unicorn
Pl = 2 # number of players
Num_Loc = 8 # number of locations (squares in a row in the grid)
SIZE = [1]*64
numIter = 1
Tolerance = 32
Stubornness = 3
# ------------------------------------------
# Here begins the action
# ------------------------------------------

# Creates the players
Players = []
for k in range(0, Pl):
	Players.append(eg.player(\
                             False,\
                             "",\
                             rp.RandomPath(SIZE),\
                             [],\
                             0, \
                             False, \
                             int(uniform(0, 1000000)), \
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

    for k in range(len(Players)):

        regions = eg.ExploreGrid(p, Num_Loc, Players,f, numIter)

        if find_min_distance_2_Focal(Players[k].path) == 0:
            if (Players[k].score < Tolerance):
                countB += 1
                if countB > Stubornness:
                    Players[k].path = rp.RandomPath(SIZE)

        else:
            Path = al.Analize(regions[k])
            Minimo, camino = find_min_distance_2_Focal(Path)
            if Minimo == 0:
                Players[k].path = camino
                countB = 0

f.close()
