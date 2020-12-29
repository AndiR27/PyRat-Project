from AIs.Node import Node
import functools

class Graph(object):

    def __init__(self, graph_dict: dict = None):
        """
        initializes a graph object
        if no dictionary or None is given, an empty dictionary will be used
        :param graph_dict: a graph in the form
        {
            "a": {"d", valeur}, etc...
        }
        """
        if graph_dict is None:
            graph_dict = {}

        self.graph_dict_Nodes = {}
        #creation des noeuds :
        self.creation_Nodes(graph_dict)

        #creations et ajout des relations :
        self.creation_relations(self.graph_dict_Nodes, graph_dict)

        self.__graph_dict: dict = self.graph_dict_Nodes
        #dict{pair, relations} -----> dict{noeud, relations}



    def __str__(self):
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


    def creation_Nodes(self, graph_dict: dict):
        #
        for key in graph_dict:
            # key = (0, 0)
            # key:list = [0, 0]
            # numeric_filter = filter(str.isdigit, key)
            # numeric_string = " ".join(numeric_filter)
            k: list = list(key)
            self.__creation_Node(k[0], k[1])
            # en plus, récuperer les valeurs et les ajouter comme relations

    def __creation_Node(self, posX: int, posY: int):
        n = Node(posX, posY)
        dico_relations = {}  # noeud, cout
        self.graph_dict_Nodes[n] = dico_relations



    def creation_relations(self, dico_noeuds:dict, dico_relations:dict):
        """

        :param dico_noeuds:
        :return:
        """
        #dico de base : {(0, 0): {(0, 1): 2}, (0, 1): {(0, 0): 2, (1, 1): 1},........}
        #notre dico de noeuds ressemble à : {noeud1: {}, noeud2: {},......}

        #il faut faire ça : {noeud1: {noeud2: 4, noeud3: 1}, noeud2: {noeud1: 4},......}
        #première boucle : dico de base sur les clés :
            #noeud 1 en (0, 0)


        for key in dico_noeuds:
            #key = noeud
            n: Node = key
            #value = dico des relations = vide pour l'instant
            for key2 in dico_relations:
                tuppleKey = (n.get_X(), n.get_Y())
                #key2 = tupple : (0, 0)
                #comparer les 2 clés : si key == key2 alors :
                # ajouter les valeurs de key2 dans value
                if key2 == tuppleKey:
                    relations:dict = dico_relations[key2]
                    # key3 étant une relation Noeud
                    relationsAvecNoeuds: dict = {}
                    for key3 in relations:
                        #trouver la ref du noeud selon les coordonnées:
                        #changer le tupple par le noeud en question

                        #res = functools.reduce(lambda sub, ele: sub * 10 + ele, key3)
                        res = '-'.join(map(str,key3))
                        n2 = self.get_Node(res, self.vertices())
                        relationsAvecNoeuds[n2] = relations[key3]
                    dico_noeuds[key] = relationsAvecNoeuds


                #break

    def get_Node(self, valNode:str, l: list):
        """

        :param valNode:
        :return:
        """
        for n in l:
            if valNode == n.get_value():
                return n

    def ajout_fromages(self, liste_fromage:list):
        """
        OPTIMISABLE
        ajout des fromages sur les nodes
        :param liste_fromage:
        :return:
        """
        #[node1, node2,etc...]
        liste_nodes = self.vertices()
        for n in liste_nodes:
            for i in liste_fromage:
                res = '-'.join(map(str, i))
                if res == n.get_value():
                    n.set_fromage()
                    break

    def voisins(self, sommet: 'Node'):
        """
        retourne tous les voisins du noeud
        :param sommet:
        :return:
        """
        if sommet in self.graph_dict_Nodes.keys():
            return self.graph_dict_Nodes[sommet].keys()
        #va retourner {sommet : {key : valeur, key : valeur}

    def get_cout(self, sommet: 'Node', voisin: 'Node') -> int:
        if sommet in self.graph_dict_Nodes.keys():
            return self.graph_dict_Nodes[sommet][voisin]


    def vertices(self) -> list:
        """
        retourne une liste de Noeuds des sommets
        :return:
        """
        return list(self.graph_dict_Nodes.keys())

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