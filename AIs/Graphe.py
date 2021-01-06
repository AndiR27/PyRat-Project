from AIs.Node import Node
#from AIs.AlgoV1 import *
import functools

class Graph(object):

    playerLocation: (int, int)
    opponentLocation: (int, int)
    ListNodes: [Node]


    def __init__(self, map: dict, playerLocation: (int, int), opponentLocation: (int, int), piecesOfCheese : [(int, int)]):
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

    def set_fromages(self, fromages: [(int, int)]):

        for f in fromages:
            n: Node = self.get_Node(f)
            n.set_fromage()

    def get_voisins(self, position: (int, int)):
        n = self.get_Node(position)
        return n.get_voisins()

    def get_voisin_cout(self, position1, position2):
        n1 = self.get_Node(position1)
        n2 = self.get_Node(position2)
        return n1.get_voisin_cout(n2)

    def set_voisins(self, map: dict):
        for key in map.keys():
            n = self.get_Node(key)
            for key2 in map[key]:
                n.set_voisins(key2, map[key][key2])

    def get_Node(self, position: (int, int)) -> 'Node':

        for n in self.ListNodes:
            if  position == n.get_coordonnes():
                return n

    def get_pos_list(self, posX: int, posY: int) -> int:
        """
        (int, int)
        Retourne la position du noeud dans la liste grâce à sa position
        """
        X = posX * 15
        posList = X + posY
        return posList


    def get_next_node(self) -> 'Node':
        """

        :return:
        """

    def set_joueurs_location(self, player: (int, int), ennemy: (int, int)):
        self.playerLocation = player
        self.opponentLocation = ennemy


    """
    def get_cout(self, sommet: 'Node') -> int:
        if sommet in self.ListNodes:
            return sommet.
    """


    def vertices_avec_fromages(self) -> list:
        """
        retourne une liste de Noeuds des sommets
        :return:
        """
        l: list = []
        for key in self.graph_dict_Nodes:
            if key.get_fromage() is True:
                l.append(key)
        return l


    def edges(self) -> list:
        """
        returns the edges of a graph
        :return:
        """
        return self.__generate_edges()

    def __generate_edges(self):
        """
        a static method generating the edges of the graph "graph"
        edges are represented as sets with one (a loop back to the vertex) or two vertices
        :return:
        """
        edges: list = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def add_vertex(self, vertex: object):
        """
        if the vertex "vertex" is not in self.__graph_dict, a key "vertex" with an empty
        dict as a value is added to the dictionary
        otherwise nothing has to be done.
        :param vertex: a vertex to add to the graph
        :return:
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = {}
            #Si on ajoute un sommet, celui-ci est lié à d'autre sommets grâce à un dico {AutreSommet, cout}

        #self.__chemins = {}
        # dicoCout : dict = {up : 0; down : 1; left: 0; right: 0} { clé = noeud : value = coût (si 0, alors c'est un mur}
        #dans le graphe :
        #boucle sur le double dico :
        #première boucle sur la clé :
        #    on crée tous les noeuds selon la clé (avec sa position)
        #deuxieme boucle :
        #on prends la valeur de la clé étant un autre dico :
        #      on y ajoute ses relations
        #      si elle existe, alors