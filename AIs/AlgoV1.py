import heapq
import itertools


from AIs.Node import Node

class PriorityQueue(object):
    _REMOVED = "<REMOVED>"

    def __init__(self):
        self.heap = []
        self.entries = {}
        self.counter = itertools.count()

    def add(self, task, priority=0):
        """Add a new task or update the priority of an existing task"""
        if task in self.entries:
            self.remove(task)

        count = next(self.counter)
        # weight = priority since heap is a min-heap
        entry = [priority, count, task]
        self.entries[task] = entry
        heapq.heappush(self.heap, entry)

    def remove(self, task):
        """ Mark the given task as REMOVED.

        Do this to avoid breaking heap-invariance of the internal heap.
        """
        entry = self.entries[task]
        entry[-1] = PriorityQueue._REMOVED

    def pop(self):
        """ Get task with highest priority.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, count, task = heapq.heappop(self.heap)
            if task is not PriorityQueue._REMOVED:
                del self.entries[task]
                return weight, task
        raise KeyError("The priority queue is empty")

    def is_empty(self):
        """
        Check if the queue is empty
        :return:
        """
        return len(self.entries) == 0



def dijkstra(graph, source: object) -> tuple:
    """
    calcule les plus courts chemins entre les sommets d'un graphe à partir d'une origine source
    graph non typé : cause des problème lié aux Importations circulaires (boucle en rond)
    :param graph: le graphe
    :param source: le sommet d'origine
    :return: une tuple avec les distance stockés dans la variable dist
                et le tableau de routage
    """
    dist: dict = {source: 0}        # Table des distances
    routage: dict = {source: None}              # table de routage
    Q: PriorityQueue = PriorityQueue()  # Creation de la Queue
    Q.add(source, priority=0)
    #enlever la première boucle -> grosse amélioration de la complexité du code au preprocessing
    """
    for v in graph.ListNodes:
        if v != source:
            dist[v] = math.inf      # unknown distance from source to v
        routage[v] = None           # predecessor of v
        Q.add(v, priority=dist[v])
    """
    while not Q.is_empty():         # Boucle de parcours sur la queue (ne sera pas vide dans que toutes les coordonnées ne seront pas faites)
        vertex: tuple = Q.pop()     # Retourne le sommet avec la plus grande priorité
        u: Node = vertex[1]

        for v in u.get_voisins():  # On prends seulement les noeuds voisins
            alt = dist[u] + u.get_voisin_cout(v)
            if v not in routage or alt < dist[v]: #vérifier si le noeud n'est pas dans la table de routage, il y sera ajouté si ce n'est pas le cas
                dist[v] = alt
                routage[v] = u
                Q.add(v, priority=alt)
    return dist, routage

def path_to(routing: dict, source: 'Node', destination: 'Node') -> list:
    """
    calcule le chemin source -> destination
    :param routing: la table de routage
    :param source: sommet source
    :param destination: sommet destination
    :return: le chemin (sans la première value correspondant à la case où l'on se trouve)
    """
    if source not in routing or destination not in routing:
        return None
    else:
        path: list = []
        #node
        cur: Node = destination
        while cur is not None:
            path.insert(0, cur)
            cur = routing[cur]
        return path[1:]

