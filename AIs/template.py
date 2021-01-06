# Template file to create an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat


###############################
# When the player is performing a move, it actually sends a character to the main program
# The four possibilities are defined here
MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

###############################
# Please put your imports here
from AIs.Graphe import Graph
from AIs.Node import Node
from AIs.AlgoV1 import *
from time import time

###############################
# Please put your global variables here
path: list = []
fromages_restants: list = []

###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict{pair(int, int), dict{pair(int, int), int}}
#clé = position de la case, val = les voisins + cout
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float

def creation_graphe(mazeMap, piecesOfCheese) -> 'Graph':
    g = mazeMap
    graph = Graph(g)
    print("Graph du projet :")

    graph.ajout_fromages(piecesOfCheese)
    #print(graph)
    return graph

def test_dijkstra(graph: 'Graph'):
    global path
    #Boucle avec x nombre d'appels de l'algo Dijkstra :
        #on aura notre distance
        #on aura la route
        #on peut calculer le chemin

    player_location: Node = graph.get_Node("0-0", graph.vertices())
    for i in graph.vertices_avec_fromages(): #liste des noeuds contenant un fromage
        #pour aller d'un point A à B :
        dist, rout = dijkstra(graph, player_location)

        #chemin = (routage, source, destination)
        path = path + path_to(rout, player_location, i)
        """
        for i in path:
            print(str(i), end=' ')
        print()
        """
        player_location = i

        #appel des directions en fonction de ce chemin pour TURN

def direction(old: (int, int), next: 'Node' ) -> chr:
    """
    Retourne la direction à prendre

    :param old: Notre position actuelle
    :param new: La position voulue
    :return: Un caractère qui défini la prochaine position voulue
    """
    new = (next.get_X(), next.get_Y())

    difference: (int, int) = (old[0] - new[0], old[1] - new[1])

    if difference == (1, 0):
        print("Gauche")
        return MOVE_LEFT
    elif difference == (-1, 0):
        print("Droite")
        return MOVE_RIGHT
    elif difference == (0, -1):
        print("Haut")
        return MOVE_UP
    elif difference == (0, 1):
        print("Bas")
        return MOVE_DOWN
    else:
        raise RuntimeError("direction: old: " + str(old) + " new: " + str(new))



###############################
# This function is not expected to return anything
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    
    # Example prints that appear in the shell only at the beginning of the game
    # Remove them when you write your own program
    global fromages_restants
    t = time()

    g = creation_graphe(mazeMap, piecesOfCheese)
    #fromages_restants = piecesOfCheese[:]
    test_dijkstra(g)
    for i in path:
        print(str(i), end=' ---> ')
    print()
    print()
    print("<b>[mazeMap]</b> " + repr(mazeMap))
    print("<b>[mazeWidth]</b> " + repr(mazeWidth))
    print("<b>[mazeHeight]</b> " + repr(mazeHeight))
    print("<b>[playerLocation]</b> " + repr(playerLocation))
    print("<b>[opponentLocation]</b> " + repr(opponentLocation))
    print("<b>[piecesOfCheese]</b> " + repr(piecesOfCheese))
    print("<b>[timeAllowed]</b> " + repr(timeAllowed))
    print(time() - t)
###############################
# Turn function
# The turn function is called each time the game is waiting
# for the player to make a decision (a move).
###############################
# Arguments are:
# mazeMap : dict(pair(int, int), dict(pair(int, int), int))
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int, int)
# playerScore : float
# opponentScore : float
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float
###############################
# This function is expected to return a move
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    
    # Example print that appears in the shell at every turn
    # Remove it when you write your own program

    #delete_fromage_pris(piecesOfCheese)
    #check_fromage_around(playerLocation, piecesOfCheese, path[0])


    next_pos = path.pop(0)

    # In this example, we always go up


    return direction(playerLocation, next_pos)


def delete_fromage_pris(piecesOfCheese):
    """
    supprime les fromages déjà pris de notre liste pour connaitre ceux encore présent dans la map
    :param piecesOfCheese:
    :return:
    """

def check_fromage_around(playerLocation, piecesOfCheese, next_position):
    """
    check si un fromage se trouve à côté du joueur pour le prendre
    :param playerLocation:
    :param piecesOfCheese:
    :return:
    """

    global path, fromages_restants
    new_pos = (next_position.get_X(), next_position.get_Y())

    f_adjacents: [(int, int)] = [(playerLocation[0] + 1, playerLocation[1]),
                               (playerLocation[0] - 1, playerLocation[1]),
                               (playerLocation[0], playerLocation[1] + 1),
                               (playerLocation[0], playerLocation[1] - 1)]

    for next_case in f_adjacents:
        if next_case not in fromages_restants or next_case == new_pos:
            f_adjacents.remove(next_case)

        #à rajouter : elif de la boue pour aller au fromage, alors on y va pas, car plus coûteux




