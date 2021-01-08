from AIs.Node import Node
from time import time
from AIs.AlgoV1 import *
import functools


class Graph(object):
    playerLocation: (int, int)
    opponentLocation: (int, int)
    ListNodes: [Node]

    def __init__(self, map: dict, playerLocation: (int, int), opponentLocation: (int, int),
                 piecesOfCheese: [(int, int)]):
        """
        initializes a graph object
        if no dictionary or None is given, an empty dictionary will be used
        :param graph_dict: a graph in the form
        {
            "a": {"d", valeur}, etc...
        }

        if graph_dict is None:
            graph_dict = {}

        self.graph_dict_Nodes = {}
        #creation des noeuds :
        self.creation_Nodes(graph_dict)

        #creations et ajout des relations :
        self.creation_relations(self.graph_dict_Nodes, graph_dict)

        self.__graph_dict: dict = self.graph_dict_Nodes
        #dict{pair, relations} -----> dict{noeud, relations}
        """
        self.playerLocation = playerLocation
        self.opponentLocation = opponentLocation
        self.ListNodes = self.__add_Nodes(map)
        self.set_fromages(piecesOfCheese)
        self.set_voisins(map)

    def __str__(self):
        """
        res: str = ""
        for key in self.graph_dict_Nodes:
            res += "Le noeud en pos " + str(key.get_X()) + " " + str(key.get_Y()) + " est relié à :\n"
            if key.get_fromage() is True:
                res += "Ce noeud a un fromage\n"
            for value in self.graph_dict_Nodes[key]:
                res += "Au noeud en pos " + str(value.get_X()) + " " + str(value.get_Y()) + " avec un coût de : " + str(
                    self.graph_dict_Nodes[key][value])+ "\n"
            res += "\n"
        return res
        """
        str_nodes = ""
        for i in self.ListNodes:
            str_nodes += i.__str__()
        return str_nodes

    def __add_Nodes(self, map: dict):
        l: [Node] = []
        for key in map.keys():
            l.append(self.__creation_Node(key))
        return l

    def __creation_Node(self, position: (int, int)):
        n: Node = Node(position, False)
        return n

    def get_all_fromages(self):
        l: list = []
        for f in self.ListNodes:
            if f.get_fromage():
                l.append(f)
        return l

    def set_fromages(self, fromages: [(int, int)]):

        for f in fromages:
            n = self.get_Node(f)
            n.set_fromage()

    def set_fromages_tour(self, fromages: [(int, int)]):
        """
        A améliorer possible de passer par les index directement ?
        - acceder directement à cette position là
        :param fromages:
        :return:
        """
        for n in self.ListNodes:
            if n.get_coordonnes() not in fromages:
                n.set_fromage_false()

    def get_voisins(self, position: (int, int)):
        n = self.get_Node(position)
        return n.get_voisins()

    def get_voisin_cout(self, position1, position2):
        n1 = self.get_Node(position1)
        n2 = self.get_Node(position2)
        return n1.get_voisin_cout(n2)

    def get_voisin_cout_node(self, n1, n2):
        if n1 in self.ListNodes and n2 in n1.get_voisins():
            return n1.get_voisin_cout(n2)

    def set_voisins(self, map: dict):
        for key in map.keys():
            n = self.get_Node(key)
            for key2 in map[key]:
                n2 = self.get_Node(key2)
                n.set_voisins(n2, map[key][key2])

    def get_Node(self, position: (int, int)) -> 'Node':
        """
                for n in self.ListNodes:
                    if  position == n.get_coordonnes():
                        return n
                """
        n: Node = Node(position, False)
        index = self.ListNodes.index(n)
        # if index in self.ListNodes:
        return self.ListNodes[index]

    def get_pos_list(self, posX: int, posY: int) -> int:
        """
        Retourne la position du noeud dans la liste grâce à sa position
        """
        X = posX * 15
        posList = X + posY
        return posList

    def get_next_node(self) -> 'Node':
        """

        :return:
        """

        global path_to

        nouveau_chemin: list = []
        n_player = self.get_Node(self.playerLocation)
        # dist, rout = dijkstra(graphMaze, n_player)
        rout = n_player.get_routes()
        dist = n_player.get_distances()

        #d'abord go check à côté
        dict_voisins = n_player.get_dico_voisins()
        for key in dict_voisins.keys():
            # check si next position ?
            if key.get_fromage() is True and dict_voisins[key] < 3:
                return key

        n_fromage = self.__prochain_fromage_plus_proche(dist, self.ListNodes)
        nouveau_chemin = path_to(rout, n_player, n_fromage)
        return nouveau_chemin[0]


    def set_joueurs_location(self, player: (int, int), ennemy: (int, int)):
        self.playerLocation = player
        self.opponentLocation = ennemy

    """
    def get_cout(self, sommet: 'Node') -> int:
        if sommet in self.ListNodes:
            return sommet.
    """

    def __prochain_fromage_plus_proche(self, distances, listnodes):
        # position de l'ennemie et ces tables de routages/disctances
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        distances_ennemy = node_ennemy.get_distances()
        dist: int = 999
        next_fromage: Node = None
        next_fromage_V2: Node = None  # fromage de secours

        # on check les fromages les plus proches de nous, pour autant qu'on soit plus prêt que l'ennemie
        for fromage in listnodes:
            if fromage.get_fromage():
                # attention à si vers la fin le joueur ennemy est plus proche des derniers fromages
                if distances[fromage] < dist and distances[fromage] <= distances_ennemy[fromage]:
                    dist = distances[fromage]
                    next_fromage = fromage
                else:
                    dist = distances[fromage]
                    next_fromage_V2 = fromage

        if next_fromage is not None:
            return next_fromage
        else:
            return next_fromage_V2

    def check_fromage_milieu(self, playerLocation, opponnentLocation, milieu: (int, int)):
        """

        :param playerLocation:
        :param opponnentLocation:
        :return:
        """
        node_milieu: Node = self.get_Node(milieu)
        node_player: Node = self.get_Node(self.playerLocation)
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        distances_player = node_player.get_distances()
        distances_ennemy = node_ennemy.get_distances()

        if node_milieu.get_fromage() == False:
            return False

        if distances_player[node_milieu] <= distances_ennemy[node_milieu]:
            return True
        else:
            return False

    def check_groupes_fromages(self, fromages_liste_full: (int, int)):
        """

        :return:
        """
        route_groupe: [Node] = [None] * 4000

        for f in self.ListNodes:
            nb_fromages: int = 0
            if f.get_fromage():
                # calcul d'une route sur 20 mouvements ? dans un rayon de 7 cases ? viser une zone avec 7 fromages atteignable facilement ?
                routes_fromage = f.get_routes()
                distances_fromage = f.get_distances()
                route_groupe_tempo: list = []
                # créer un chemin complet jusqu'à avoir 7 fromages pour trouver celui le plus opti
                while nb_fromages < 7:
                    # destination = prochain fromage le plus pres :
                    # on ne veut que les distances des fromages dans notre dico :
                    new_data = {k: v for k, v in distances_fromage.items() if k.get_fromage() == True}
                    del new_data[f]
                    f.set_fromage_false()
                    destination: Node = min(new_data, key=new_data.get)
                    route_groupe_tempo = route_groupe_tempo + path_to(routes_fromage, f, destination)
                    nb_fromages += 1
                    f = destination
                    routes_fromage = f.get_routes()
                    distances_fromage = f.get_distances()

                if len(route_groupe_tempo) < len(route_groupe):
                    route_groupe = route_groupe_tempo
                else:
                    pass
                self.set_fromages(fromages_liste_full)

        for i in route_groupe:
            print(str(i), end=' ')
        print()
        return route_groupe