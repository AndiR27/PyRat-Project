class Node:

    def __init__(self, position: (int, int), cheese: bool):

        # 5-10
        self.__coordonnes : (int, int) = position
        self.__cheese : bool = cheese
        self.__voisins : dict = {}
        #= {down : 1} { clé = noeud : value = coût} (si mur, alors noeud pas dans le dico)
        self.__routes : dict = {}
        self.__distances: dict = {}

    def __str__(self):
        str_fromage = ""
        if self.__cheese == True:
            str_fromage += "+ fromage"
        return "case en : " + str(self.__coordonnes) + str_fromage + " "

    def get_coordonnes(self):
        return self.__coordonnes

    def get_Node(self, position: (int, int)):
        return self

    def get_dico_voisins(self):
        return self.__voisins

    def get_voisins(self):
        return self.__voisins.keys()

    def get_voisin_cout(self, n: 'Node') -> int:
        return self.__voisins[n]

    def set_voisins(self, n : 'Node', cout : int):
        self.__voisins[n] = cout

    def get_fromage(self):
        return self.__cheese

    def set_fromage(self):
        self.__cheese = True

    def set_fromage_false(self):
        self.__cheese = False

    def get_routes(self):
        return self.__routes

    def set_routes(self, routes: dict):
        self.__routes = routes

    def get_distances(self):
        return self.__distances

    def set_distances(self, dist: dict):
        self.__distances = dist

    def __eq__(self, other):
        if isinstance(other, Node):
            return other.__coordonnes == self.__coordonnes
        else:
            return False

    def __hash__(self):
        return hash(self.__coordonnes)
