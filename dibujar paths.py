from sys import argv
print "Initializing pandas..."
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

data_archivo = "sim_dat.csv"

Num_Loc = int(raw_input("> Numero de locaciones: ")) #4, 6
Num_Graf = int(raw_input("> Numero de experimentos a graficar: ")) #1, 2


# Opens the file with data from DCL experiment and parses it into data
print "Leyendo datos..."
#data = pd.read_csv(data_archivo, sep='\t', header=0)
# data = pd.read_csv('../Datos/' + data_archivo, index_col=False)
data = pd.read_csv(data_archivo, index_col=False)
#data = pd.read_csv(data_archivo, index_col=False)
print "Datos leidos!"
print data[:3]

# Find total times for locations visited
print "Finding total visits to locations..."
cols = ['a' + str(i+1) + str(j+1) for i in range(0, Num_Loc) for j in range(0, Num_Loc)]
visited_players = {}
for key, p in data.groupby(['Player']):
    visited_players[key] = [p[x].sum() for x in cols]
    # print "Jugador " + str(key) + " visito " + str(visited_players[key])

# Produce graphics
print "Producing graphics..."
Contador = 0
for KEY, GRP in data.groupby(['Exp']):
    for Key, Grp in GRP.groupby(['Dyad']):

        # figs for visited locations
        fig4, axes4 = plt.subplots(1,2)
        for a in axes4:
            a.get_xaxis().set_visible(False)
            a.get_yaxis().set_visible(False)

        # Plot per player
        i = 0
        for key, grp in Grp.groupby(['Player']):
            # Plot visited locations
            print "Dibujando visited locations de la pareja " + str(Key)
            step = 0.25
            ejemp = visited_players[key]
            m = max(ejemp)

            tangulos = []
            for j in range(0, len(ejemp)):
                x = int(j) % 4
                y = (int(j) - x) / 4
            #    print "x: " + str(x)
            #    print "y: " + str(y)
                by_x = x * step
                by_y = 1 - (y + 1) * step
            #    print "by_x: " + str(by_x)
            #    print "by_y: " + str(by_y)
                tangulos.append(patches.Rectangle(*[(by_x, by_y), step, step], facecolor="black", alpha=float(ejemp[j])/m))
            for p in tangulos:
                axes4[i].add_patch(p)
            axes4[i].set_title('Player ' + str(key))

            i += 1

        fig4.savefig('Graficas/' + str(Key) + '_visited_locations' + str(KEY) + '.pdf')
        Contador += 1
        if Contador >= Num_Graf: break
