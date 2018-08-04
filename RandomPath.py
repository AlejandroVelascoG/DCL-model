print "Importing packages..."
from random import random, sample
import numpy as np
import csv
import matplotlib.pyplot as plt
# import pandas as pd
print "Ready!"

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
