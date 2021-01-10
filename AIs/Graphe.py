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
        Constructeur de la classe Graph
        :param map: la Map du labyrinthe
        :param playerLocation: la position du joueur
        :param opponentLocation: la position de l'ennemie
        :param piecesOfCheese: la liste des fromages
        """
        self.playerLocation = playerLocation
        self.opponentLocation = opponentLocation
        self.ListNodes = self.__add_Nodes(map)
        self.set_fromages(piecesOfCheese)
        self.set_voisins(map)

    def __str__(self):
        """
        le to_string() de la classe Graph
        :return:
        """
        str_nodes = ""
        for i in self.ListNodes:
            str_nodes += i.__str__()
        return str_nodes

    def __add_Nodes(self, map: dict):
        """
        methode privée nous permettant d'ajouter les sommets du labyrinthe comme étant un Node
        :param map:
        :return:
        """
        l: [Node] = []
        for key in map.keys():
            l.append(self.__creation_Node(key))
        return l

    def __creation_Node(self, position: (int, int)) -> 'Node':
        """
        Création du Node
        :param position:
        :return: le Node créé
        """
        n: Node = Node(position, False)
        return n


    def set_fromages(self, fromages: [(int, int)]):
        """
        Définis les noeud ayant un fromage dans notre graph
        :param fromages: la liste des fromages encore présents dans le labyrinthe
        :return:
        """

        for f in fromages:
            n = self.get_Node(f)
            n.set_fromage()

    def set_fromages_tour(self, fromages: [(int, int)]):
        """
        Methode qui défini les fromages ayant été pris dans notre graphe (valeur du Node == False si celui-ci n'a plus de fromage)
        A améliorer possible de passer par les index directement ?
        - acceder directement à cette position là
        :param fromages: la liste contenant les fromages restants
        :return:
        """
        for n in self.ListNodes:
            if n.get_coordonnes() not in fromages:
                n.set_fromage_false()

    def get_voisins(self, position: (int, int)) -> 'Node':
        """
        Methode permettant de récupérer les Node voisins à une position donnée
        :param position: la position de la case voulu
        :return: les Nodes voisins
        """
        n = self.get_Node(position)
        return n.get_voisins()


    def get_voisin_cout_node(self, n1, n2) -> int:
        """
        Permet de récuperer le coût de passage d'un node à un autre
        :param n1: le premier Node
        :param n2: le deuxième Node voisin au premier
        :return: le coût entre les 2
        """
        if n1 in self.ListNodes and n2 in n1.get_voisins():
            return n1.get_voisin_cout(n2)

    def set_voisins(self, map: dict):
        """
        Défini à la creation du graph, les voisins de tous les sommets de notre Graph
        :param map: la map contenant toutes les infos du labyrinthe
        """
        for key in map.keys():
            n = self.get_Node(key)
            for key2 in map[key]:
                n2 = self.get_Node(key2)
                n.set_voisins(n2, map[key][key2])

    def get_Node(self, position: (int, int)) -> 'Node':
        """
        Permet de récupérer le Node de la position voulue
        :param position: la case souhaitée
        :return: le Node correspondant à la case
        """
        """
        Cette methode était utilisée au départ : avec les index, on a gagné BEAUCOUP de temps
        for n in self.ListNodes:
            if position == n.get_coordonnes():
                return n
        """
        n: Node = Node(position, False)
        index = self.ListNodes.index(n)
        return self.ListNodes[index]


    def set_joueurs_location(self, player: (int, int), ennemy: (int, int)):
        """
        Défini dans notre Graph la localisation de notre joueur et de l'ennemie
        :param player: Nous
        :param ennemy: L'adversaire
        """
        self.playerLocation = player
        self.opponentLocation = ennemy


    def get_next_node(self, playerScore: int, piecesOfCheese: (int, int), go_milieu: bool, go_zone: bool) -> 'Node':
        """
        Methode principale du mouvement : va définir selon un certains nombre de paramètres, le prochain Node sur lequel notre
        joueur doit aller
        :param playerScore: le score du joueur
        :param piecesOfCheese: la liste des fromages restants
        :param go_milieu: boolean pour déterminer si il doit aller au milieu
        :param go_zone: boolean pour déterminer quand est-ce qu'il doit check la meilleure zone et y aller
        :return: le node de la prochaine case où il doit aller
        """
        global path_to

        source: Node = self.get_Node(self.playerLocation)

        # d'abord go check à côté
        next_move_around = self.check_around(source)
        if next_move_around is not None:
            return next_move_around

        #strat de départ == go milieu tant que go_milieu est True
        if go_milieu is True:
            next_move_go_milieu = self.route_milieu((10, 7))
            return next_move_go_milieu

        #aller dans la zone si au milieu ou si go_milieu est False
        if go_zone is True:
            zones_all = self.groupes_fromages_zones(piecesOfCheese)
            zone_opti = self.choisirZone(zones_all)
            next_move_zone = self.prochain_fromage_zone(zone_opti)
            self.cpt_zone += 1
            return next_move_zone

        #Lorsqu'on est proche de la victoire, check la meilleure route possible à prendre pour aller chercher les 3 derniers fromages

        if playerScore >= 18 and len(piecesOfCheese) > 3:
            print("mode")
            destination: Node = self.mode_end_fast(piecesOfCheese)
            nouveau_chemin = path_to(source.get_routes(), source, destination)
            return nouveau_chemin[0]
        #sinon dans la plupart des coups, on va jusqu'au prochain fromage
        else:
            return self.prochain_fromage()

    def check_around(self, source):
        """
        Methode permettant de vérifier si un Node a un voisin avec un fromage ou un voisin du voisin a un fromage
        :param source: la position à laquelle on se trouve
        :return: la next position à aller (si il y en a une)
        """
        dict_voisins = source.get_dico_voisins()
        for key in dict_voisins.keys():
            # check si next position ?
            if key.get_fromage() is True and dict_voisins[key] <= 2:
                return key

        #Obligée de passer par une deuxième boucle pour éviter que la souris tourne en boucle entre 2 cases
        #comme cela, on s'assure de vérifier d'abord si les voisins (key) ont un fromage ou pas, si ce n'est pas le cas, cette deuxième boucle sera lancée
        for key in dict_voisins.keys():
            if key.get_fromage() is False:
                dict_voisins2 = key.get_dico_voisins()
                for key2 in dict_voisins2.keys():
                    if key2.get_fromage() is True and dict_voisins2[key2] == 1:
                        return key

    def route_milieu(self, milieu: (int, int)):
        """
        Définis le prochain Node à prendre pour aller au milieu
        :param milieu:
        :return:
        """

        n_player = self.get_Node(self.playerLocation)
        n_milieu = self.get_Node(milieu)
        route = path_to(n_player.get_routes(), n_player, n_milieu)
        return route[0]

    def prochain_fromage(self):
        """
        déterminer le prochain fromage que notre souris doit viser
        :param self: le graph
        :return: le Node de la prochaine position
        """
        n_player = self.get_Node(self.playerLocation)
        rout = n_player.get_routes()
        dist = n_player.get_distances()
        n_fromage = self.__prochain_fromage_plus_proche(dist, self.ListNodes)
        nouveau_chemin = path_to(rout, n_player, n_fromage)
        return nouveau_chemin[0]

    def prochain_fromage_zone(self, zone):
        """
        déterminer le prochain fromage de la zone opti que la souris doit viser
        :param self:
        :return:le node de la next position
        """
        n_player = self.get_Node(self.playerLocation)
        rout = n_player.get_routes()
        dist = n_player.get_distances()
        n_fromage = self.__prochain_fromage_plus_proche(dist, zone)
        nouveau_chemin = path_to(rout, n_player, n_fromage)
        return nouveau_chemin[0]

    def __prochain_fromage_plus_proche(self, distances, listnodes):
        """
        Fonction privée permettant de calculer la distance du prochain fromage le plus petit, et plus proche de nous que de l'adversaire
        :param distances: la table des distances selon notre position
        :param listnodes: la liste des Nodes à prendre en compte pour la recherche du next fromage
        :return: le Node du fromage que la souris doit viser
        """
        # Position de l'ennemie et ces tables de routages/distances
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
        #next_fromage_V2 permet d'avoir un fromage de secours au cas ou l'ennemie est proche de tous les fromages restants (on choisit
        #ainsi tout même le fromage le plus proche et on va vers lui)
        if next_fromage is not None:
            return next_fromage
        else:
            return next_fromage_V2

    def check_fromage_milieu(self, milieu: (int, int)) -> bool:
        """
        Verifie si le fromage du milieu est toujours là et si il est atteignable avant l'ennemie
        :param milieu: la position du fromage au milieu qui est fixe
        :return boolean nous disant si c'est toujours ok d'aller au milieu
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

    def groupes_fromages_zones(self, piecesOfCheese) -> [[]]:
        """
        Methode où l'on découpe notre labyrinthe en zone afin d'y stocker les fromages dans des listes correspondant aux zones
        :param piecesOfCheese: la liste des fromages
        :return: une matrice contenant les différentes listes (une pour chaque zone)
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
        Permet de choisir la zone opti dans laquelle notre souris doit se rendre selon la position ennemie, le nombre de fromages restants
        :param zones_all: la liste contenant les listes de zones
        :return: la meilleure zone où se rendre
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

    def __zone_position_ennemi(self) -> str:
        """
        Détermine la zone dans laquelle se trouve l'ennemie (on évitera ainsi d'aller là bas pour ne pas perdre du temps)
        :return: le nom de la zone à éviter
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
        Calcule parmis les zones possible, celle contenant le plus de fromage
        :param zones: les différentes zones
        :return: la meilleure zone
        """
        best_zone = zones[0]
        for zone in zones:
            if len(zone) > len(best_zone):
                best_zone = zone
        return best_zone

    def mode_end_fast(self, piecesOfCheese):
        """
        Methode s'activant vers la fin pour finir au plus vite au lieu d'aller simplement vers le fromage le plus proche
        Au lieu d'aller au fromage le plus proche (qui peut risquer d'être seul dans un coin) on va faire un peu plus de distance pour récupérer les 3 derniers fromages
        Principe : check distance fromage proche + son next fromage + son next fromage
        :param piecesOfCheese: la liste des fromages encore présents sur la map
        :return: la prochaine position que la souris doit prendre
        """
        distance_min = math.inf
        route_prio_end: list = []
        node_player: Node = self.get_Node(self.playerLocation)
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        #on calcule d'abord la distance entre notre position - un des fromages dans la liste
        for f in piecesOfCheese:
            f_node = self.get_Node(f)
            nb_fromages: int = 0
            routes_fromage = f_node.get_routes()
            distances_fromage = f_node.get_distances()
            # if distances_fromage[node_player] <= distances_fromage[node_ennemy]:
            route_groupe_tempo: list = []
            route_groupe_tempo = route_groupe_tempo + path_to(node_player.get_routes(), node_player, f_node)
            nb_fromages += 1
            # créer un chemin complet jusqu'à avoir 3 fromages pour trouver celui le plus opti
            while nb_fromages <= 2:
                # destination = prochain fromage le plus pres :
                # on ne veut que les distances des fromages dans notre dico :
                # on crée ainsi un dico temporaire contenant simplement les distances d'un noeud aux autres fromages (permet de récupérer facilement la valeur min)
                new_data = {k: v for k, v in distances_fromage.items() if k.get_fromage() == True}
                #ne pas oublier de supprimer le fromage sur lequel on se trouve (car celui-ci a une distance de 0, on ne veut pas le prendre en compte)
                del new_data[f_node]
                f_node.set_fromage_false()
                destination: Node = min(new_data, key=new_data.get)
                #Ajout de la route vers le fromage d'après
                route_groupe_tempo = route_groupe_tempo + path_to(routes_fromage, f_node, destination)
                nb_fromages += 1
                #ne pas oublier de définir notre nouvelle position ainsi que les tables de routages/distances
                f_node = destination
                routes_fromage = f_node.get_routes()
                distances_fromage = f_node.get_distances()

            #la route contenant le moins de déplacement sera prise en compte
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
        Définir un dico contenant les strats possible de l'adversaire
        [à améliorer, mais pas eu le temps]
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

    def __strat_milieu(self) -> list:
        """
        Définis le chemin que l'adversaire doit prendre pour aller au milieu le plus vite
        :return: liste contenant la route à prendre
        """
        list_chemin = []
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        list_chemin.append(node_ennemy)
        n_milieu = self.get_Node((10, 7))
        rout = node_ennemy.get_routes()
        list_chemin = path_to(rout, node_ennemy, n_milieu)

        return list_chemin

    def __strat_next_fromage_basique(self):
        """
        Définis le chemin que l'adversaire doit prendre si il ne fait que choisir les fromages les plus proches tour par tour pendant 15 tours

        :return: le chemin "basique" de l'ennemie
        """
        list_chemin = []
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        routes = node_ennemy.get_routes()
        distances = node_ennemy.get_distances()
        while len(list_chemin) <= 15:
            # destination = prochain fromage le plus pres :
            # on ne veut que les distances des fromages dans notre dico :
            new_data = {k: v for k, v in distances.items() if k.get_fromage() == True}
            #del new_data[node_ennemy]
            node_ennemy.set_fromage_false()
            destination: Node = min(new_data, key=new_data.get)
            list_chemin = list_chemin + path_to(routes, node_ennemy, destination)
            node_ennemy = destination
            del new_data[node_ennemy]

            routes = node_ennemy.get_routes()
            distances = node_ennemy.get_distances()

        return list_chemin

    def mouvements_adversaires(self, mouvements_ennemie_liste):
        """
        check les mouvements de l'adversaires pour ensuite les comparer à des stratégies qu'il peut prendre : on s'adapte en fonction de cela
        on met juste à jour les déplacements de l'ennemie dans une liste
        :param mouvements_ennemie_liste: la liste contenant les mouvements de l'ennemi
        :return:la liste des déplacements mise à jour
        """
        node_ennemy: Node = self.get_Node(self.opponentLocation)
        #on ne prends pas sa position de départ
        if node_ennemy.get_coordonnes() != (20, 14):
            mouvements_ennemie_liste.append(node_ennemy)
        return mouvements_ennemie_liste

    def comparer_mouvements(self, list_mouvements: [], dico_strat: {}) -> str:
        """
        comparer mouvements du joueur ennemie avec des strats hypothetiques
        :param list_mouvements: les mouvements du joueurs qu'il a fait depuis le début
        :param dico_strat: un dictionnaire contenant plusieurs strats possible des bases pouvant être prises par l'ennemie
        :return:le nom de la strat ennemie prise
        """

        #comparaison avec le dictionnaire des strats créé au début
        for key in dico_strat.keys():
            list_hypo = dico_strat[key]
            strat = self.__comparer_mouvements_liste(list_mouvements, list_hypo)
            if strat is True:
                return key
        return "pas de strat prédéfinie"


    def __comparer_mouvements_liste(self, list_mouvements, list_hypo):
        """
        compare 2 listes entre elles pour vérifier si les mouvements sont les mêmes
        :param list_mouvements: les mouvements du joueur
        :param list_hypo: les mouvements hypothétique créé par nous au preprocessing
        :return: un boolean pour savoir si les listes sont identiques ou pas
        """
        strat: bool = True
        for i in range(0, len(list_mouvements) - 1):
            if list_mouvements[i] != list_hypo[i]:
                return False
        return strat
