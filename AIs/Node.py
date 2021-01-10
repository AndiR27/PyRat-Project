class Node:

    def __init__(self, position: (int, int), cheese: bool):
        """
        constructeur de la classe Node
        :param position: coordonnées de la position
        :param cheese: est-ce que la Node a un fromage (faux par défaut)
        """
        self.__coordonnes : (int, int) = position
        self.__cheese : bool = cheese
        self.__voisins : dict = {}
        # = {down : 1} { clé = noeud : value = coût} (si mur, alors noeud pas dans le dico)
        self.__routes : dict = {}
        self.__distances: dict = {}

    def __str__(self):
        """
        méthode d'affichage de la classe Node
        :return: l'affichage souhaité du Node
        """
        str_fromage = ""
        if self.__cheese:
            str_fromage += "+ fromage"
        return "case en : " + str(self.__coordonnes) + str_fromage + " "

    def get_coordonnes(self):
        """
        getter des coordonnées du Node
        :return: les coordonnées du Node
        """
        return self.__coordonnes

    def get_dico_voisins(self):
        """
        getter des voisins du Node
        :return: un dictionnaire contenant les voisins du Node
        """
        return self.__voisins

    def get_voisins(self):
        """
        getter des voisins du Node
        :return: les voisins du Node
        """
        return self.__voisins.keys()

    def get_voisin_cout(self, n: 'Node') -> int:
        """
        getter du coût entre deux positions
        :param n: Node voisin du Node self
        :return: le cout entre self et n
        """
        return self.__voisins[n]

    def set_voisins(self, n : 'Node', cout : int):
        """
        setter de voisins, permet de définir les voisins du Node
        :param n: Node que l'on souhaite avoir en voisin
        :param cout: cout entre self et n
        """
        self.__voisins[n] = cout

    def get_fromage(self) -> bool:
        """
        getter de fromage, permet de vérifier si un Node possède un fromage
        :return: True si contient un fromage, False si n'en contient pas
        """
        return self.__cheese

    def set_fromage(self):
        """
        setter de fromage, permet d'attribuer un fromage a un Node
        """
        self.__cheese = True

    def set_fromage_false(self):
        """
        setter de fromage à False, permet d'attribuer du vide à un Node
        """
        self.__cheese = False

    def get_routes(self):
        """
        getter de routes, permet de récupérer la table de routage du Node
        :return: la table de routage du Node
        """
        return self.__routes

    def set_routes(self, routes: dict):
        """
        setter de routes, permet d'attribuer une table de routage à un Node
        :param routes: dictionnaire contenant la table de routage
        """
        self.__routes = routes

    def get_distances(self):
        """
        getter des distances, permet de récupérer la table des distances du Node
        :return: la table des distances
        """
        return self.__distances

    def set_distances(self, dist: dict):
        """
        setter de distances, permet d'attribuer une table de distances à un Node
        :param dist: dictionnaire contenant la table des distances
        """
        self.__distances = dist

    def __eq__(self, other):
        """
        méthode equals qui vérifie si deux instances de Node sont les mêmes
        :param other: l'autre Node que l'on souhaite comparer
        :return: True ou False selon le résultat
        """
        if isinstance(other, Node):
            return other.__coordonnes == self.__coordonnes
        else:
            return False

    def __hash__(self):
        """
        méthode qui retourne la version hashée des coordonées d'un Node
        :return: hashage des coordonnées d'un Node
        """
        return hash(self.__coordonnes)
