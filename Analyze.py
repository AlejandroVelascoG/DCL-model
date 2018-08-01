print "loading packages..."
import RandomPath as rp

def separateTiles(visitedTiles):
    '''
    Input: visitedTiles es una lista con 0s (no visito), 1s (visito solo el jugador),
    2s (ambos jugadores visitaron)
    Output: soloTiles, jointTiles
    '''
    print "Aqui viene lo que esta haciendo Miguel"

def analyze(visitedTiles, FocalPaths, Treshold, SIZE):
    '''

    '''

    soloTiles, jointTiles = separateTiles(visitedTiles)

    d = closest(soloTiles)

    if d < Treshold:


    rp.RandomPath(SIZE)
