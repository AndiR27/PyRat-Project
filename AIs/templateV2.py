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
graphMaze: Graph
path: list = []
fromages_restants: list = []
nbr_fromages: int = 41

###############################
# Preprocessing function
# The preprocessing function is called at the start of a game
# It can be used to perform intensive computations that can be
# used later to move the player in the maze.
###############################
# Arguments are:
# mazeMap : dict{pair(int, int), dict{pair(int, int), int}}
# clé = position de la case, val = les voisins + cout
# mazeWidth : int
# mazeHeight : int
# playerLocation : pair(int, int)
# opponentLocation : pair(int,int)
# piecesOfCheese : list(pair(int, int))
# timeAllowed : float

def creation_graphe(mazeMap, playerLocation, opponentLocation, piecesOfCheese) -> 'Graph':

    graphMaze = Graph(mazeMap, playerLocation, opponentLocation, piecesOfCheese)
    print("Graph du projet :")
    print(graphMaze)

    # print(graph)
    return graphMaze


def test_dijkstra(playerLocation):
    global path
    # Boucle avec x nombre d'appels de l'algo Dijkstra :
    # on aura notre distance
    # on aura la route
    # on peut calculer le chemin

    """
    for i in graphMaze.ListNodes:  # liste de tous les noeuds
        if i.get_fromage() == True:
            # pour aller d'un point A à B :
            dist, rout = dijkstra(graphMaze, i)
            i.set_routes(rout)
            i.set_distances(dist)
        # chemin = (routage, source, destination)
        #path = path + path_to(rout, player_location, i)
    """

    n_player = graphMaze.get_Node(playerLocation)
    n_milieu = graphMaze.get_Node((10, 7))
    dist, rout = dijkstra(graphMaze, n_player)
    print("clés de route")
    for key, v in rout.items():
        print(key, end='->')
        print(v)

    print("clés de dist")
    for key, v in dist.items():
        print(key, end='->')
        print(v)
    path = path_to(rout, n_player, n_milieu)

        #player_location = i

        # appel des directions en fonction de ce chemin pour TURN

def test_dijkstra_tour(playerLocation, piecesOfCheese):
    global path
    # Boucle avec x nombre d'appels de l'algo Dijkstra :
    # on aura notre distance
    # on aura la route
    # on peut calculer le chemin


    n_player = graphMaze.get_Node(playerLocation)
    dist, rout = dijkstra(graphMaze, n_player)
    n_fromage = prochain_fromage_plus_proche(piecesOfCheese, rout, dist)
    path = path_to(rout, n_player, n_fromage)

        #player_location = i

        # appel des directions en fonction de ce chemin pour TURN

def prochain_fromage_plus_proche(piecesOfCheese, distances):
    dist: int = 999
    next_fromage: Node = None
    for fromage in piecesOfCheese:
        f = graphMaze.get_Node(fromage)
        if distances[f] < dist:
            dist = distances[f]
            next_fromage = f

    return next_fromage

def direction(old: (int, int), next: 'Node') -> chr:
    """
    Retourne la direction à prendre

    :param old: Notre position actuelle
    :param new: La position voulue
    :return: Un caractère qui défini la prochaine position voulue
    """
    new = next.get_coordonnes()

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
    global fromages_restants, graphMaze, path
    t = time()

    graphMaze = creation_graphe(mazeMap, playerLocation, opponentLocation, piecesOfCheese)
    fromages_restants = piecesOfCheese[:]
    test_dijkstra(playerLocation)
    for i in path:
        print(str(i), end=' ')
    print()

    #prends un chemin : par exemple, va au milieu ou go pour le meilleur groupe de fromages

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
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese,
         timeAllowed):
    global graphMaze, path, nbr_fromages
    # Example print that appears in the shell at every turn
    # Remove it when you write your own program

    # Check la position adverse
    # aller au mileu ? peut être plus opti (mais faire attention si l'adversaire va aussi au milieu)


    # géner l'adversaire ?
    # créer la route avec le groupe de fromage opti
    #
    #delete_fromage_pris(playerLocation, opponentLocation)
    #verifier si y a un fromage à côté et si c'est pas trop chiant d'aller le chercher :


    graphMaze.set_joueurs_location(playerLocation, opponentLocation)
    graphMaze.set_fromages_tour(piecesOfCheese)
    if (10,7) not in piecesOfCheese:
        test_dijkstra_tour(playerLocation, piecesOfCheese)
    #chaque tour, t'as la liste des fromages : [(10,7), (2,6),...]
    #après avoir pris le fromage du milieu, t'as la liste des fromages : [(2,6),...]

    # check_fromage_around(playerLocation, piecesOfCheese, path[0], mazeMap)

    next_pos = path.pop(0)

    # In this example, we always go up

    return direction(playerLocation, next_pos)


def delete_fromage_pris(playerLocation, opponentLocation):
    """
    supprime les fromages déjà pris de notre liste pour connaitre ceux encore présent dans la map
    :param piecesOfCheese:
    :return:
    """

    if playerLocation in fromages_restants:
        fromages_restants.remove(playerLocation)
    if opponentLocation in fromages_restants:
        fromages_restants.remove(opponentLocation)



def check_fromage_around(playerLocation, piecesOfCheese, next_position, map):
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

        # à rajouter : elif de la boue pour aller au fromage, alors on y va pas, car plus coûteux
        else:
            # check lien entre playerLocation et next_case : graphe[playerLocation][next_case]
            #test si y a un mur
            # case 1 : relié à case 2, 3, 4 ; case 2 : relié à 1 5 6
            if next_case not in map[playerLocation].keys():
                f_adjacents.remove(next_case)
            #test si boue :
            elif map[playerLocation][next_case] > 1:
                f_adjacents.remove(next_case)

            #alors on go sur le fromage, on l'ajoute à notre route par defaut
            else:
                new_case : Node #la prochaine case avec le fromage à prendre
                prev_case: Node #la case ou se trouvait le joueur avant d'aller sur le fromage
                new_case = transform_to_node(next_case)
                prev_case = transform_to_node(playerLocation)
                path.insert(0, prev_case)
                path.insert(0, new_case)






def transform_to_node(case) -> 'Node':
    """
    transformer la case au noeud en question :
    :param case:
    :return:
    """
    res = '-'.join(map(str, case))

    return graphMaze.get_Node(res, graphMaze.vertices())


#TODO QUESTIONS :
# gérer le node pour qu'il connaisse les routes/distances ?
# utilité du graphe ?
# création de l'arbre ?
# dijkstra sur toutes les cases vers chaque fromage ? comment stocker ses données ?
# methode de viser le milieu, puis un groupe ?


#TODO REPONSES :
# faire dijkstra à chaque tour ? peut etre meilleur
# aller au milieu c'est pas trop mal et pas génant
# calculer les chemins entre les fromages : si fromage pris, on recalcule le chemin juste pour un fromage
#pour le graphe : avoir seulement un tableau de noeud (plus besoin d'utiliser un dico)
# dans le graphe il faut créer avec le constr, getNode(), getVoisins(), getNextNode() pour se deplacer sur la case suivante
# pour le noeud : avoir un dico voisin avec les voisins du noeud

#si l'adversaire va plutôt vers la zone de fromages, go le géner ?