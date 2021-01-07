import heapq
import itertools
import math
import time
import random
from time import time
from pprint import pprint
from heapq import heappush, heappop

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

    def peek(self):
        """ Check task with highest priority, without removing.

        :return: Priority, Task with highest priority
        """
        while self.heap:
            weight, count, task = self.heap[0]
            if task is PriorityQueue._REMOVED:
                heapq.heappop(self.heap)
            else:
                return weight, task

        return None

    def is_empty(self):
        """
        Check if the queue is empty
        :return:
        """
        return len(self.entries) == 0

    def __str__(self):
        temp = [str(e) for e in self.heap if e[-1] is not PriorityQueue._REMOVED]
        return "[%s]" % ", ".join(temp)


def dijkstra(graph, source: object) -> tuple:
    """
    calcule les plus courts chemins entre les sommets d'un graphe à partir d'une origine source
    graph non typé : cause des problème lié aux Importations circulaires (boucle en rond)
    :param graph: le graphe
    :param source: le sommet d'origine
    :return: une tuple avec les distance stockés dans la variable dist
                et le tableau de routage
    """
    dist: dict = {source: 0}        # initialization
    routage: dict = {source: None}              # routing table
    Q: PriorityQueue = PriorityQueue()  # create vertex priority queue Q
    Q.add(source, priority=0)
    #enlever la première boucle
    """
    for v in graph.ListNodes:
        if v != source:
            dist[v] = math.inf      # unknown distance from source to v
        routage[v] = None           # predecessor of v
        Q.add(v, priority=dist[v])
    """
    while not Q.is_empty():         # the main loop
        vertex: tuple = Q.pop()     # remove and return best vertex
        u: Node = vertex[1]

        for v in u.get_voisins():  # only v that are still in Q
            alt = dist[u] + u.get_voisin_cout(v)
            if v not in routage or alt < dist[v]:
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
    :return: le chemin
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

