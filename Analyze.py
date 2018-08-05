print "loading packages..."
import RandomPath as rp

def separateTiles(visitedTiles):
    '''
    Input: visitedTiles es una lista con 0s (no visito), 1s (visito solo el jugador),
    2s (ambos jugadores visitaron)
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
            
    #print "Aqui viene lo que esta haciendo Miguel"

##def analyze(visitedTiles, FocalPaths, Treshold, SIZE):
##    '''
##
##    '''
##
##    soloTiles, jointTiles = separateTiles(visitedTiles)
##
##    d = closest(soloTiles)
##
##    if d < Treshold:
##
##
##    rp.RandomPath(SIZE)
print separateTiles([0,1,2,2,0,1,1])
