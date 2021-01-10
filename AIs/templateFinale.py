# Template file to create an AI for the game PyRat
# http://formations.telecom-bretagne.eu/pyrat
TEAM_NAME: str = "La Kabuki Squad"


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
strategies_ennemie_possibles = {}
mouvements_ennemie: list = []
go_milieu: bool = True
go_zone: bool = False



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


def initialisation_Dijkstra():
    """
    Initialisation de tous les Node pour connaître
    :return:
    """
    # Boucle avec x nombre d'appels de l'algo Dijkstra :
    # on aura notre distance
    # on aura la route
    # on peut calculer le chemin

    for i in graphMaze.ListNodes:  # liste de tous les noeuds
        # if i.get_fromage() == True:
        # pour aller d'un point A à B :
        dist, rout = dijkstra(graphMaze, i)
        i.set_routes(rout)
        i.set_distances(dist)


"""
CHOIX DE DEPART - au début contenait un chemin de base à prendre, mais PAS DU TOUT OPTI, le fait de changer sa route à chaque tour en fonction
de la situation est clairement plus optimale que de suivre une route préfaite selon 2-3 critères, la fonction suivant n'est ainsi pas utilisée

def choix_du_chemin_depart(route_groupe: list, playerLocation):
    
    check si c'est mieux d'aller sur le groupe de fromages (si plus proche), sinon on va plutôt aller au milieu et ensuite on avisera
    :param route_groupe:
    :param playerLocation:
    :return:
    
    global route_depart
    # position de joueur = le start lors du preprocessing
    n_depart = graphMaze.get_Node(playerLocation)
    routes_depart = n_depart.get_routes()
    distances_depart = n_depart.get_distances()

    if distances_depart[route_depart[-1]] > distances_depart[route_groupe[0]]:
        #print("On va vers le groupe de fromage")
        # si la route pour aller au milieu est plus longue, autant aller direct vers notre groupe de fromage, donc rajouter path_to jusqu'au premier fromage du groupe
        destination: Node = route_groupe[0]
        chemin_jusquau_groupe = path_to(routes_depart, n_depart, destination)

        route_depart = chemin_jusquau_groupe[:-1] + route_groupe
    else:
        print("On va au milieu")
"""

def direction(old: (int, int), next: 'Node') -> chr:
    """
    Retourne la direction à prendre

    :param old: Notre position actuelle
    :param new: La position voulue (sous forme de Node)
    :return: la direction devant être prise pour accéder au prochain Node
    """
    new = next.get_coordonnes()

    diff: (int, int) = (old[0] - new[0], old[1] - new[1])

    if diff == (-1, 0):
        return MOVE_RIGHT
    elif diff == (1, 0):
        return MOVE_LEFT
    elif diff == (0, -1):
        return MOVE_UP
    elif diff == (0, 1):
        return MOVE_DOWN
    else:
        #permet de voir si la souris saute un tour ou pas
        raise RuntimeError("direction: old: " + str(old) + " new: " + str(new))


###############################
# This function is not expected to return anything
def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):

    global fromages_restants, graphMaze, route_depart, strategies_ennemie_possibles

    t = time()

    # création de notre graphe
    graphMaze = Graph(mazeMap, playerLocation, opponentLocation, piecesOfCheese)

    # implémentation des routes/distances de tous les noeuds avec Dijkstra
    initialisation_Dijkstra()

    # definir les possibles stratégies basiques de l'ennemie après un certain nombre de tours :
    #dico : { "nom de la strat" : [mouvements],}
    strategies_ennemie_possibles = graphMaze.strats_ennemie()
    graphMaze.set_fromages(piecesOfCheese)

    # on reset correctement nos noeuds avec les fromages
    graphMaze.set_fromages(piecesOfCheese)




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
    global graphMaze, go_milieu, mouvements_ennemie, strategies_ennemie_possibles, go_zone


    # aller au mileu ? peut être plus opti (mais faire attention si l'adversaire va aussi au milieu)

    #Gérer les positions : de notre souris, de l'adversaire, des fromages :
    graphMaze.set_joueurs_location(playerLocation, opponentLocation)
    graphMaze.set_fromages_tour(piecesOfCheese)

    #stocker
    graphMaze.groupes_fromages_zones(piecesOfCheese)

    mouvements_ennemie = graphMaze.mouvements_adversaires(mouvements_ennemie)
    if len(mouvements_ennemie) == 15:

        strat_ennemie = graphMaze.comparer_mouvements(mouvements_ennemie, strategies_ennemie_possibles )
        if strat_ennemie == "StratMilieu":
            f_mid = graphMaze.check_fromage_milieu((10, 7))
            if f_mid is True:
                go_milieu = True
                go_zone = False
            else:
                go_milieu = False
                go_zone = True
        elif strat_ennemie == "StratProchainFromage":
            go_milieu = True
            go_zone = False
        else:
            go_milieu = True
            go_zone = False

    f_mid = graphMaze.check_fromage_milieu((10, 7))

    #différents test pour verifier si cela est toujours utile d'aller au milieu (doit être changé à False sinon notre souris ne bougera pas)
    if f_mid is False or (10,7) not in piecesOfCheese or (playerLocation == (10,7) and opponentLocation==(10,7) or playerLocation == (10,7)):
        go_milieu = False
    # check si le joueur est dans la zone pour prendre les fromage, lorsqu'il est dans la zone, il prends les fromages les plus proches à la suite
    if graphMaze.cpt_zone >= 15:
        go_zone = False

    next_pos = graphMaze.get_next_node(playerScore, piecesOfCheese, go_milieu, go_zone)

    return direction(playerLocation, next_pos)



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
