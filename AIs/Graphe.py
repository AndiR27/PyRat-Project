from AIs.Node import Node
from time import time
from AIs.AlgoV1 import *
import functools
import math


class Graph(object):
    playerLocation: (int, int)
    opponentLocation: (int, int)
    ListNodes: [Node]
    cpt_zone = 0
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

    def set_joueurs_location(self, player: (int, int), ennemy: (int, int)):
        self.playerLocation = player
        self.opponentLocation = ennemy

    """
    def get_cout(self, sommet: 'Node') -> int:
        if sommet in self.ListNodes:
            return sommet.
    """

    def get_next_node(self, playerScore: int, piecesOfCheese: (int, int), go_milieu: bool, go_zone: bool) -> 'Node':
        """

        :return:
        """
        global path_to

        print("milieu :" + str(go_milieu))
        print("zone :" + str(go_zone))
        source: Node = self.get_Node(self.playerLocation)

        # d'abord go check à côté
        next_move_around = self.check_around(source)
        if next_move_around is not None:
            return next_move_around

        # sinon strat de départ == go milieu tant que
        if go_milieu is True:
            next_move_go_milieu = self.route_milieu((10, 7))

        #aller dans la zone si au milieu ou si go_milieu est False
        if go_zone is True:
            zones_all = self.groupes_fromages_zones(piecesOfCheese)
            zone_opti = self.choisirZone(zones_all)
            next_move_zone = self.prochain_fromage_zone(zone_opti)
            self.cpt_zone += 1
            return next_move_zone


        if playerScore >= 18:
            destination: Node = self.mode_end_fast(piecesOfCheese)
            nouveau_chemin = path_to(source.get_routes(), source, destination)
            return nouveau_chemin[0]
        else:
            return self.prochain_fromage()

    def check_around(self, source):
        """

        :return:
        """
        dict_voisins = source.get_dico_voisins()
        for key in dict_voisins.keys():
            # check si next position ?
            if key.get_fromage() is True and dict_voisins[key] <= 2:
                return key

        for key in dict_voisins.keys():
            if key.get_fromage() is False:
                dict_voisins2 = key.get_dico_voisins()
                for key2 in dict_voisins2.keys():
                    if key2.get_fromage() is True and dict_voisins2[key2] == 1:
                        return key

    def route_milieu(self, milieu: (int, int)):

        n_player = self.get_Node(self.playerLocation)
        n_milieu = self.get_Node(milieu)
        route = path_to(n_player.get_routes(), n_player, n_milieu)
        return route[0]

    def prochain_fromage(self):
        """
        déterminer le prochain fromage
        :param self:
        :return:
        """
        n_player = self.get_Node(self.playerLocation)
        rout = n_player.get_routes()
        dist = n_player.get_distances()
        n_fromage = self.__prochain_fromage_plus_proche(dist, self.ListNodes)
        nouveau_chemin = path_to(rout, n_player, n_fromage)
        return nouveau_chemin[0]

    def prochain_fromage_zone(self, zone):
        """
        déterminer le prochain fromage
        :param self:
        :return:
        """
        n_player = self.get_Node(self.playerLocation)
        rout = n_player.get_routes()
        dist = n_player.get_distances()
        n_fromage = self.__prochain_fromage_plus_proche(dist, zone)
        nouveau_chemin = path_to(rout, n_player, n_fromage)
        return nouveau_chemin[0]

    def __prochain_fromage_plus_proche(self, distances, listnodes):
        # position de l'ennemie et ces tables de routages/distances
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        distances_ennemy = node_ennemy.get_distances()
        dist = math.inf
        next_fromage: Node = None
        next_fromage_V2: Node = None  # fromage de secours

        # on check les fromages les plus proches de nous, pour autant qu'on soit plus prêt que l'ennemie
        for case in listnodes:
            if case.get_fromage():
                # attention à si vers la fin le joueur ennemy est plus proche des derniers fromages
                if distances[case] < dist and distances[case] <= distances_ennemy[case]:
                    dist = distances[case]
                    next_fromage = case
                else:
                    dist = distances[case]
                    next_fromage_V2 = case

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
                while nb_fromages < 5:
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

    def groupes_fromages_zones(self, piecesOfCheese) -> [[]]:
        """

        :param piecesOfCheese:
        :return:
        """
        zoneA: list = []  # entre (0,0) et (10,7), zone prio
        zoneB: list = []  # entre (0, 8) et (10, 14), next zone prio ?
        zoneC: list = []  # entre (11, 0) et (20, 7), zone proche de l'ennemie
        zoneD: list = []  # entre (11, 8) et (20, 14), zone de l'ennemi - mauvais plan
        for f in piecesOfCheese:
            f_node = self.get_Node(f)
            if 0 <= f[0] <= 10 and 0 <= f[1] <= 7:
                zoneA.append(f_node)
            elif 0 <= f[0] <= 10 and 8 <= f[1] <= 14:
                zoneB.append(f_node)
            elif 11 <= f[0] <= 20 and 0 <= f[1] <= 7:
                zoneC.append(f_node)
            else:
                zoneD.append(f_node)
        zones: list = [zoneA, zoneB, zoneC, zoneD]
        return zones

    def choisirZone(self, zones_all):
        """

        :param zones_all:
        :return:
        """
        zone_ennemi = self.__zone_position_ennemi()
        #zoneA, zoneB, zoneC, zoneD = zones_all[0][1][2][3]
        if zone_ennemi == "ZoneA":
            del zones_all[0]
            meilleure_zone: list = self.__meilleure_zone(zones_all)
            print(meilleure_zone)
        elif zone_ennemi == "ZoneB":
            del zones_all[1]
            meilleure_zone: list = self.__meilleure_zone(zones_all)
        elif zone_ennemi == "ZoneC":
            del zones_all[2]
            meilleure_zone: list = self.__meilleure_zone(zones_all)
        else:
            del zones_all[3]
            meilleure_zone: list = self.__meilleure_zone(zones_all)

        return meilleure_zone

    def __zone_position_ennemi(self):
        """

        :return:
        """
        ennemie = self.opponentLocation
        if 0 <= ennemie[0] <= 10 and 0 <= ennemie[1] <= 7:
            return "ZoneA"
        elif 0 <= ennemie[0] <= 10 and 8 <= ennemie[1] <= 14:
            return "ZoneB"
        elif 11 <= ennemie[0] <= 20 and 0 <= ennemie[1] <= 7:
            return "ZoneC"
        else:
            return "ZoneD"

    def __meilleure_zone(self, zones) -> list:
        """

        :param zones:
        :return:
        """
        best_zone = zones[0]
        for zone in zones:
            if len(zone) > len(best_zone):
                best_zone = zone
        return best_zone

    def mode_end_fast(self, piecesOfCheese):
        """
        Au lieu d'aller au fromage le plus proche (qui peut risquer d'être seul dans un coin) on va faire un peu plus de distance pour récupérer les 3 derniers fromages
        Principe : check distance fromage proche + son next fromage + son next fromage
        :return:
        """
        distance_min = math.inf
        route_prio_end: list = []
        node_player: Node = self.get_Node(self.playerLocation)
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        for f in piecesOfCheese:
            f_node = self.get_Node(f)
            nb_fromages: int = 0
            routes_fromage = f_node.get_routes()
            distances_fromage = f_node.get_distances()
            # if distances_fromage[node_player] <= distances_fromage[node_ennemy]:

            route_groupe_tempo: list = []
            # créer un chemin complet jusqu'à avoir 3 fromages pour trouver celui le plus opti
            while nb_fromages <= 2:
                # destination = prochain fromage le plus pres :
                # on ne veut que les distances des fromages dans notre dico :
                new_data = {k: v for k, v in distances_fromage.items() if k.get_fromage() == True}
                del new_data[f_node]
                f_node.set_fromage_false()
                destination: Node = min(new_data, key=new_data.get)
                route_groupe_tempo = route_groupe_tempo + path_to(routes_fromage, f_node, destination)
                nb_fromages += 1
                f_node = destination
                routes_fromage = f_node.get_routes()
                distances_fromage = f_node.get_distances()

            if len(route_groupe_tempo) < distance_min:
                distance_min = len(route_groupe_tempo)
                route_prio_end = route_groupe_tempo
            else:
                pass
            self.set_fromages(piecesOfCheese)

        # tester si l'ennemie se trouve plus proche de cette mini-zone, on go au next fromage et tampis

        destination: Node = route_prio_end[0]
        if node_player.get_distances()[destination] <= node_ennemy.get_distances()[destination]:
            return destination
        else:
            return self.prochain_fromage()

    def strats_ennemie(self):
        """

        :return:
        """
        dico_strats_ennemie: dict = {}
        # strat d'aller au milieu :
        list = self.__strat_milieu()
        dico_strats_ennemie["StratMilieu"] = list

        # strat de juste faire les fromages les plus proches à la suite depuis le départ
        list2 = self.__strat_next_fromage_basique()
        dico_strats_ennemie["StratProchainFromage"] = list2

        return dico_strats_ennemie

    def __strat_milieu(self):
        list_chemin = []
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        list_chemin.append(node_ennemy)
        n_milieu = self.get_Node((10, 7))
        rout = node_ennemy.get_routes()
        list_chemin = path_to(rout, node_ennemy, n_milieu)

        return list_chemin

    def __strat_next_fromage_basique(self):
        list_chemin = []
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        routes = node_ennemy.get_routes()
        distances = node_ennemy.get_distances()
        new_data = {k: v for k, v in distances.items() if k.get_fromage() == True}
        destination: Node = min(new_data, key=new_data.get)
        list_chemin = list_chemin + path_to(routes, node_ennemy, destination)
        node_ennemy = destination
        routes = node_ennemy.get_routes()
        distances = node_ennemy.get_distances()
        while len(list_chemin) <= 15:
            # créer un chemin complet jusqu'à avoir 7 fromages pour trouver celui le plus opti
            # destination = prochain fromage le plus pres :
            # on ne veut que les distances des fromages dans notre dico :
            new_data = {k: v for k, v in distances.items() if k.get_fromage() == True}
            del new_data[node_ennemy]
            node_ennemy.set_fromage_false()
            destination: Node = min(new_data, key=new_data.get)
            list_chemin = list_chemin + path_to(routes, node_ennemy, destination)
            node_ennemy = destination
            routes = node_ennemy.get_routes()
            distances = node_ennemy.get_distances()
        return list_chemin

    def mouvements_adversaires(self, mouvements_ennemie_liste):
        """
        check les mouvements de l'adversaires pour ensuite les comparer à des stratégies qu'il peut prendre : on s'adapte en fonction de cela

        :return:
        """
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        if node_ennemy.get_coordonnes() != (20, 14):
            mouvements_ennemie_liste.append(node_ennemy)
        return mouvements_ennemie_liste

    def comparer_mouvements(self, list_mouvements: [], dico_strat: {}) -> str:
        """
        comparer mouvements du joueur ennemie avec des strats hypothetiques
        :param list_mouvements:
        :param dico_strat:
        :return:
        """

        for key in dico_strat.keys():
            list_hypo = dico_strat[key]
            strat = self.__comparer_mouvements_liste(list_mouvements, list_hypo)
            if strat is True:
                return key

    def __comparer_mouvements_liste(self, list_mouvements, list_hypo):
        strat: bool = True
        for i in range(0, len(list_mouvements) - 1):
            if list_mouvements[i] != list_hypo[i]:
                return False
        return strat
