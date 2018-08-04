print "loading packages..."
from random import choice, uniform, random, sample, randint, shuffle
from math import floor
import numpy as np
from RandomPath import RandomPath
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# Define de players
class player(object):
	'''Object defining a player. Has the following properties:
		Ready; Decision; path; where; score'''
	def __init__(self, Ready, Decision, path, Name, Where, Accuracy):
		self.ready = Ready # True or false
		self.decision = Decision # "Present" or "Absent"
		self.path = path # List of 0s and 1s
		self.name = Name # Name of player
		self.where = Where # Tiles actually visited
		self.accuracy = Accuracy # True or False: Whether the player's decision is correct

def ExploreGrid(probUnicorn, Num_Loc, Players, f, round):
    '''
    Explores the grid with both players and determines the score

    Input:  probUnicorn, probability of there being a unicorn
    Num_Loc, grid of size Num_Loc * Num_Loc
    Players, which is a list of players
    f, opened file to write the development of the game
    round, number of the round being played

    Output: paths, list of two lists with the tiles visited by players
    Score, list of two scores
    '''
	# The variables that return the player's scores and joint thorughout the rounds
	# Jugador0_score = []
	# Jugador1_score = []
	# Joints = []

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
