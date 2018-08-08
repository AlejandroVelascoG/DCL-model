# Objects and functions for the model of division of cognitive labor
# with focal pahts.
# Edgar Andrade, Miguel Valencia, Juan Camilo Hoyos
# 2018

print "loading packages..."
from random import uniform, random, sample, shuffle
from math import floor
import numpy as np

# ------------------------------------------
# Objects
# ------------------------------------------
# Define de players
class player(object):
	'''Object defining a player. Has the following properties:
		Ready; Decision; path; where; score'''
	def __init__(self, Ready, Decision, path, Name, Where, Accuracy, Score):
		self.ready = Ready # True or false
		self.decision = Decision # "Present" or "Absent"
		self.path = path # List of 0s and 1s
		self.name = Name # Name of player
		self.where = Where # Tiles actually visited
		self.accuracy = Accuracy # True or False: Whether the player's decision is correct
		self.score = Score # Player's score



# ------------------------------------------
# Functions
# ------------------------------------------

def set_distance(l1, l2, Num_Loc):
    # Finds the distance between lists l1 and l2
    # Lists l1 and l2 must contain only 0 and 1
	# Num_Loc is the number of rows in the grid

    intersect = np.sum([np.where(l1[i] + l2[i] > 1, 1, 0) for i in range(0, Num_Loc * Num_Loc)])
    # print "Intersection: " + str(intersect)
    uni = np.sum([np.where(l1[i] + l2[i] > 0, 1, 0) for i in range(0, Num_Loc * Num_Loc)])
    # print "Union: " + str(uni)
    if uni == 0:
        return 0
    else:
        return 1 - (float(intersect)/uni)

def find_min_distance_2_Focal(path, Num_Loc):
    '''
    Finds the minimum distance from a path to a focal path

    Input: path is a list with path followed
		   Num_Loc is the number of rows in the grid

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
    D_2_UP = set_distance(path, UP, Num_Loc)
    D_2_DOWN = set_distance(path, DOWN, Num_Loc)
    D_2_LEFT = set_distance(path, LEFT, Num_Loc)
    D_2_RIGHT = set_distance(path, RIGHT, Num_Loc)
    D_2_ALL = set_distance(path, ALL, Num_Loc)
    D_2_NOTHING = set_distance(path, NOTHING, Num_Loc)
    D_2_IN = set_distance(path, IN, Num_Loc)
    D_2_OUT = set_distance(path, OUT, Num_Loc)
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

def separateTiles(visitedTiles, Num_Loc):
    '''
    Input: visitedTiles es una lista con 0s (no visito), 1s (visito solo el jugador),
    	   2s (ambos jugadores visitaron)
		   Num_Loc is the number of rows in the grid

    Output: soloTiles, jointTiles
    '''
    soloTiles = []
    jointTiles = []
    for i in visitedTiles:
        if i==1:
            soloTiles.append(1)
            jointTiles.append(0)
        elif i==2:
            soloTiles.append(0)
            jointTiles.append(1)
        else:
            soloTiles.append(0)
            jointTiles.append(0)
    return soloTiles, jointTiles

def analyze(visitedTiles, Threshold, SIZE, Num_Loc):
	'''
	Comentarios

    Input: ?????????????
		   Num_Loc is the number of rows in the grid
	'''
	soloTiles, jointTiles = separateTiles(visitedTiles, Num_Loc)
	distance, path = find_min_distance_2_Focal(soloTiles, Num_Loc)

	if distance < Threshold:
		return path
	else:
		distance, path = find_min_distance_2_Focal(jointTiles, Num_Loc)
		if distance < Threshold:
			return [1 - i for i in path]
		else:
			return RandomPath(SIZE)

def ExploreGrid(probUnicorn, Num_Loc, Players, f, round):
    '''
    Explores the grid with both players and determines the score

    Input:  probUnicorn, probability of there being a unicorn
    Num_Loc, grid of size Num_Loc * Num_Loc
    Players, which is a list of players
    f, opened file to write the development of the game
    round, number of the round being played

    Output: paths, list of two lists with the tiles visited by Players
    		Modifies .score, .where, . path from Players
    '''

    # Creates dyad name
    dyad = str(Players[0].name)[:3] + '-' + str(Players[1].name)[:3]

	#Initializing the players for the round
    for pl in Players:
		pl.decision = "Absent"
		pl.where = []
		pl.ready = False
		pl.score = 0
		pl.accuracy = False

	# Initializing the board
    Board = [0 for l in range(0, Num_Loc * Num_Loc)]
    # print "Board: ", Board
    # print "len(Board): ", len(Board)

	# Determine whether there is a unicorn and where
    place = -1
    # print "probUnicorn", probUnicorn
    x = uniform(0, 1)
    # print "Random: ", x
    if x > probUnicorn:
        place = int(floor(uniform(0, Num_Loc * Num_Loc - 1)))
        Board[place] = 1
        print "There is a unicorn at " + str(place)
    else:
        print "There is NO unicorn"

    # Finding maximum length of players' paths
    n = np.sum(Players[0].path)
    m = np.sum(Players[1].path)
    max_length_paths = max(n, m)
    # print "max_length_paths:", max_length_paths

    # Creating a random order to follow path
    Order = []
    for pl in Players:
        # Finds the tiles to be explored by player pl and creates
        # a randomly ordered list with these indexed tiles
        region = [i for i, j in enumerate(pl.path) if j == 1]
        shuffle(region)
        Order.append(region)
    print "Order[0]: ", Order[0]
    print "Order[1]: ", Order[1]

    # Start searchging for the unicorn
    for j in range(max_length_paths):
        print "\nRunning iteration " + str(j)
        for k in range(0, len(Players)):
            # See if other player said present. If so, do the same
            if Players[1 - k].decision == "Present":
                Players[k].decision = "Present"
                print "Player " + str(k) + " said Present"
                Players[k].ready = True
                break
                # If the other player did not say Present, and
                # current player is not ready, then...
            elif not Players[k].ready:
                # ...look at the location determined by the path
                #				print "Player " + str(k) + " is using path: " + \
                #					str(Players[k].path)
                # See if the strategy is not over...
                # print "Iteration: ", j
                # print "Length path: ", np.sum(Players[k].path)
                # print "Player: ", k
                if j < np.sum(Players[k].path):
                    search_place = Order[k][j] # Order[k] was defined before as the random order to follow Players[k].path
                    Players[k].where.append(search_place)
                    print "Player " + str(k) + " is searching at " + str(search_place)
                    if Board[search_place] == 1:
                        Players[k].decision = "Present"
                        print "Player " + str(k) + " said Present"
                        Players[k].ready = True
                    else: print "Player " + str(k) + " found no unicorn"
            # Chechk if both players are ready. If so, stop search
            elif Players[1-k].ready == True:
                break
        else: continue
        break

	# Determine locations visited by both players
    a =  [x for x in Players[0].where if x in Players[1].where]
    print "Both: ", a
    print "len(both): ", len(a)

    # Determine the tiles visited by each player as a list of 0s and 1s
    # 0 means the player did not visited the tile
    # 1 means the player did visit the tile
    # 2 means both players visited the tile
    Regions = [[], []]
    for j in range(Num_Loc * Num_Loc):
        for k in range(len(Players)):
            if j in Players[k].where:
                if j in Players[1 - k].where:
                    Regions[k].append(2)
                else:
                    Regions[k].append(1)
            else:
                Regions[k].append(0)

    print "Regions[0]: ", Regions[0]
    print "Regions[1]: ", Regions[1]

    # Determine individual scores
    for k in range(0, len(Players)):
		f.write(dyad + ",") # Dyad
		f.write(str(round + 1) + ",") # Round

		# print "Player " + str(k) + " checked " + str(len(Players[k].where)) + " locations"
		# print "Player " + str(k) + "\'s answer was: " + Players[k].decision
		if place == -1:
			# print "There was NO unicorn"
			if Players[k].decision == "Absent":
				print "Player " + str(k) + "\'s answer is Correct!"
				Players[k].accuracy = True
				Players[k].score = Num_Loc*Num_Loc/2 - len(a)
				print "Player " + str(k) + "\'s score this round is: " + \
					str(Players[k].score)
			else:
				print "Player " + str(k) + "\'s answer is Incorrect!"
				Players[k].accuracy = False
				Players[k].score = -Num_Loc*Num_Loc - len(a)
				print "Player " + str(k) + "\'s score this round is: " + \
					str(Players[k].score)
		else:
			# print "There was a unicorn"
			if Players[k].decision == "Present":
				print "Player " + str(k) + "\'s answer is Correct!"
				Players[k].accuracy = True
				Players[k].score = Num_Loc*Num_Loc/2 - len(a)
				print "Player " + str(k) + "\'s score this round is: " + \
					str(Players[k].score)
			else:
				print "Player " + str(k) + "\'s answer is Incorrect!"
				Players[k].accuracy = False
				Players[k].score = -Num_Loc*Num_Loc - len(a)
				print "Player " + str(k) + "\'s score this round is: " + \
					str(Players[k].score)
		f.write(str(Players[k].name) + ",") # Player
		f.write(Players[k].decision + ",") # Answer
		f.write(str(len(Players[k].where)) + ",") # Time
		for l in range(0, Num_Loc * Num_Loc):
			if l in Players[k].where:
				f.write("1,") # If visited location
			else:
				f.write("0,") # If not visited location
		for l in range(0, Num_Loc * Num_Loc):
			if l in Players[k].where:
				f.write(str(Players[k].where.index(l) + 1) + ",") # The time when he visited location
			else:
				f.write("0,") # If not visited location
		f.write(str(Players[k].score) + ",") # Score
		f.write(str(len(a)) + ",") # Joint
		if place == -1:
			f.write("Unicorn_Absent" + ",") # Is_there
			f.write("-1" + ",") # where_x
			f.write("-1" + "\n") # where_y
		else:
			f.write("Unicorn_Present" + ",") # Is_there
			x = place % Num_Loc
			y = (place - x) / Num_Loc
			f.write(str(x) + ",") # where_x
			f.write(str(y) + "\n") # where_y and End of line

    return Regions[0], Regions[1]

def comprobarExploreGrid():
    ''' Check whether the function ExploreGrid is working fine
        Input:  p, probability of there being a unicorn
                Num_Loc, grid of size Num_Loc * Num_Loc
                Players, which is a list of players
                f, opened file to write the development of the game
                round, number of the round being played
                dyad, name of the dyad

        Output:
    '''

    p = 0.5
    Num_Loc = 3
    Pl = 2

    SIZE = [1] * (Num_Loc * Num_Loc)
    # print "SIZE: ", SIZE

    Players = []
    for k in range(0, Pl):
        args = [False, "Absent", RandomPath(SIZE), randint(0, 1000), [], False]
        # print len(args)
        Players.append(player(*args))
        print "Player" + str(Players[-1].name) + "path: " + str(Players[-1].path)

    dyad = str(Players[0].name)[:3] + '-' + str(Players[1].name)[:3]

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

    round = 1


    paths = [[], []]
    paths[0], paths[1] = ExploreGrid(p, Num_Loc, Players, f, round)

    # Produce graphics
    print "Producing graphics..."
    # figs for visited locations
    fig4, axes4 = plt.subplots(1,2)
    for a in axes4:
        a.get_xaxis().set_visible(False)
        a.get_yaxis().set_visible(False)

    # Plot per player
    i = 0
    for pl in Players:
        # Plot visited locations
        print "Dibujando visited locations de la pareja " + str(dyad)
        step = float(1) / Num_Loc
        tangulos = []
        for j in range(Num_Loc * Num_Loc):
            x = int(j) % Num_Loc
            y = (int(j) - x) / Num_Loc
            #    print "x: " + str(x)
            #    print "y: " + str(y)
            by_x = x * step
            by_y = 1 - (y + 1) * step
            #    print "by_x: " + str(by_x)
            #    print "by_y: " + str(by_y)
            if paths[i][j] == 0:
                colores = "white"
            elif paths[i][j] == 1:
                colores = "black"
            elif paths[i][j] == 2:
                colores = "red"
            else:
                print "We have a problem: path player " + str(pl.Name) + " not right!"

            # print "Color: ", colores
            tangulos.append(patches.Rectangle(*[(by_x, by_y), step, step], facecolor=colores))

        for t in tangulos:
            axes4[i].add_patch(t)
            axes4[i].set_title('Player ' + str(Players[i].name))

        i += 1

    f.close()

    # fig4.show()
    plt.show()

def weighted_choice(weights):
    '''
    Returns a number with probability determined by weights
    Simple linear approach from
    https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python
    '''
    totals = []
    running_total = 0
    for w in weights:
        running_total += w
        totals.append(running_total)
    # rnd = random.random() * running_total
    rnd = random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i

def RandomPath(SIZE):
    '''
    Input: SIZE which is the distribution of number of tiles visited
           SIZE must be a list of the frequencies/weight for each size

    Output: PATH which is a random path whose number of tiles depends on SIZE
    '''

    Num_Rows = len(SIZE) ** 0.5
    assert Num_Rows == int(Num_Rows), "Oops, problems with lenght of SIZE"
    Num_Rows = int(Num_Rows)

    grid = range(0, Num_Rows * Num_Rows)
    n = weighted_choice(SIZE)
    Casillas_a_visitar = sample(grid, n)
    path = []
    for i in range(0, Num_Rows * Num_Rows):
        if i in Casillas_a_visitar:
            path.append(1)
        else:
            path.append(0)

    return path

def comprobarRandomPath(SIZE, n):
    '''
    Input: SIZE must be a list of the frequencies/weight for each size
              n must be the number of times to try the RandomPath function
    Output: A histogram with the sizes obtained by repeating
            n times the RandomPath function
    '''
    print "Checking correctness of RandomPath..."
    sizesObtained = []
    for i in range(0, n):
        l = np.sum(RandomPath(SIZE))
        sizesObtained.append(l)

    # print sizesObtained

    x = np.array(sizesObtained)
    counts = np.bincount(x).tolist()
    # print counts

    x = range(len(SIZE))
    width = 1/1.5
    f, axarr = plt.subplots(1,2)
    axarr[0].bar(x, SIZE, width, color = 'blue')
    axarr[1].bar(x, counts, width, color = 'blue')
    # plt.title("SIZE Histogram")
    # plt.xlabel("Size")
    # plt.ylabel("Frequency")
    plt.show()
