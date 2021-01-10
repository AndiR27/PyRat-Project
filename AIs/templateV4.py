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
route_depart: list = []

fromages_restants: list = []
nbr_fromages: int = 41
go_milieu: bool = True


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


def initialisation_dijkstra(playerLocation):
    global route_depart
    # Boucle avec x nombre d'appels de l'algo Dijkstra :
    # on aura notre distance
    # on aura la route
    # on peut calculer le chemin



    for i in graphMaze.ListNodes:  # liste de tous les noeuds ou y a un fromage
        # if i.get_fromage() == True:

        # pour aller d'un point A à B :
        dist, rout = dijkstra(graphMaze, i)
        i.set_routes(rout)
        i.set_distances(dist)

        # chemin = (routage, source, destination)
        # path = path + path_to(rout, player_location, i)

        # player_location = i

        # appel des directions en fonction de ce chemin pour TURN


def choix_du_chemin_depart(route_groupe: list, playerLocation):
    """
    check si c'est mieux d'aller sur le groupe de fromages (si plus proche), sinon on va plutôt aller au milieu et ensuite on avisera
    :param route_groupe:
    :param playerLocation:
    :return:
    """
    global route_depart
    # position de joueur = le start lors du preprocessing
    n_depart = graphMaze.get_Node(playerLocation)
    routes_depart = n_depart.get_routes()
    distances_depart = n_depart.get_distances()

    if distances_depart[route_depart[-1]] > distances_depart[route_groupe[0]]:
        print("On va vers le groupe de fromage")
        # si la route pour aller au milieu est plus longue, autant aller direct vers notre groupe de fromage, donc rajouter path_to jusqu'au premier fromage du groupe
        destination: Node = route_groupe[0]
        chemin_jusquau_groupe = path_to(routes_depart, n_depart, destination)

        route_depart = chemin_jusquau_groupe[:-1] + route_groupe
    else:
        print("On va au milieu")


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
        return MOVE_LEFT
    elif difference == (-1, 0):
        return MOVE_RIGHT
    elif difference == (0, -1):
        return MOVE_UP
    elif difference == (0, 1):
        return MOVE_DOWN
    else:
        raise RuntimeError("direction: old: " + str(old) + " new: " + str(new))


###############################
# This function is not expected to return anything
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    # Example prints that appear in the shell only at the beginning of the game
    # Remove them when you write your own program
    global fromages_restants, graphMaze, route_depart

    t = time()

    # création de notre graphe
    graphMaze = Graph(mazeMap, playerLocation, opponentLocation, piecesOfCheese)

    # implémentation des routes/distances de tous les noeuds avec Dijkstra + chemin pour aller au milieu
    initialisation_dijkstra(playerLocation)

    # check des meilleurs groupes de fromage pour en obtenir 5 rapidement
    # dico
    route_groupe = graphMaze.check_groupes_fromages(piecesOfCheese)

    #choix_du_chemin_depart(route_groupe, playerLocation)

    # on reset correctement nos noeuds avec les fromages
    graphMaze.set_fromages(piecesOfCheese)

    # prends un chemin : par exemple, va au milieu ou go pour le meilleur groupe de fromages

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
    global graphMaze, route_depart, go_milieu, nbr_fromages
    # Example print that appears in the shell at every turn
    # Remove it when you write your own program
    t = time()
    # Check la position adverse
    # aller au mileu ? peut être plus opti (mais faire attention si l'adversaire va aussi au milieu)

    # géner l'adversaire ?
    # créer la route avec le groupe de fromage opti
    #
    # delete_fromage_pris(playerLocation, opponentLocation)
    # verifier si y a un fromage à côté et si c'est pas trop chiant d'aller le chercher :

    graphMaze.set_joueurs_location(playerLocation, opponentLocation)
    graphMaze.set_fromages_tour(piecesOfCheese)
    #go_milieu = graphMaze.check_fromage_milieu(playerLocation, opponentLocation, (10, 7))
    #if ((10, 7) not in piecesOfCheese and go_milieu == False) or len(route_depart) == 0 or changement_route(route_depart) is True:

    next_pos = graphMaze.get_next_node(playerScore, piecesOfCheese)

    # check_fromage_around(playerLocation, piecesOfCheese, route_depart[0], mazeMap)


    return direction(playerLocation, next_pos)

def changement_route(rte: list) -> bool:
    """

    :param rte:
    :return:
    """

    for l in rte:
        if l.get_fromage() is True:
            return True

    return False




def check_fromage_around(playerLocation, piecesOfCheese, next_position):
    """
    check si un fromage se trouve à côté du joueur pour le prendre
    :param playerLocation:
    :param piecesOfCheese:
    :return:
    """

    global route_depart, fromages_restants

    f_adjacents: [(int, int)] = [(playerLocation[0] + 1, playerLocation[1]),
                                 (playerLocation[0] - 1, playerLocation[1]),
                                 (playerLocation[0], playerLocation[1] + 1),
                                 (playerLocation[0], playerLocation[1] - 1)]
    player_node: Node = graphMaze.get_Node(playerLocation)

    for next_case in f_adjacents:
        if 0 <= next_case[0] <= 20 or 0 <= next_case[1] <= 14:
            f_adjacents.remove(next_case)
        else:
            # noeud de la prochaine case : (ça arrive que ça bug ?? wtf)
            next_case_node: Node = graphMaze.get_Node(next_case)
            if next_case_node.get_fromage() is False or next_case == next_position.get_coordonnes():
                f_adjacents.remove(next_case)

            # à rajouter : elif de la boue pour aller au fromage, alors on y va pas, car plus coûteux
            else:
                # check lien entre playerLocation et next_case : graphe[playerLocation][next_case]
                # test si y a un mur
                # case 1 : relié à case 2, 3, 4 ; case 2 : relié à 1 5 6
                if next_case_node not in player_node.get_voisins():
                    f_adjacents.remove(next_case)
                # test si boue :
                elif player_node.get_voisin_cout(next_case_node) > 1:
                    f_adjacents.remove(next_case)

                # alors on go sur le fromage, on l'ajoute à notre route par defaut
                else:
                    # la case ou se trouvait le joueur avant d'aller sur le fromage
                    print("CANCEL DRIFTU FROMAGE")
                    route_depart.insert(0, player_node)
                    # la prochaine case avec le fromage à prendre
                    route_depart.insert(0, next_case_node)


def check_fromage_aroundV2(playerLocation, piecesOfCheese, next_position):
    """
    check si un fromage se trouve à côté du joueur pour le prendre
    :param playerLocation:
    :param piecesOfCheese:
    :return:
    """

    global route_depart, fromages_restants
    player_node: Node = graphMaze.get_Node(playerLocation)
    #voisins du noeud où on se trouve :
    dict_voisins = player_node.get_dico_voisins()
    for key in dict_voisins.keys():
        #check si next position ?
        if key != next_position and key.get_fromage() is True and dict_voisins[key] < 3:
            # la case ou se trouvait le joueur avant d'aller sur le fromage
            print("CANCEL DRIFTU FROMAGE")
            route_depart.insert(0, player_node)
            # la prochaine case avec le fromage à prendre
            route_depart.insert(0, key)

# TODO QUESTIONS :
# gérer le node pour qu'il connaisse les routes/distances ?
# utilité du graphe ?
# création de l'arbre ?
# dijkstra sur toutes les cases vers chaque fromage ? comment stocker ses données ?
# methode de viser le milieu, puis un groupe ?


# TODO REPONSES :
# faire dijkstra à chaque tour ? peut etre meilleur
# aller au milieu c'est pas trop mal et pas génant
# calculer les chemins entre les fromages : si fromage pris, on recalcule le chemin juste pour un fromage
# pour le graphe : avoir seulement un tableau de noeud (plus besoin d'utiliser un dico)
# dans le graphe il faut créer avec le constr, getNode(), getVoisins(), getNextNode() pour se deplacer sur la case suivante
# pour le noeud : avoir un dico voisin avec les voisins du noeud

# si l'adversaire va plutôt vers la zone de fromages, go le géner ?
