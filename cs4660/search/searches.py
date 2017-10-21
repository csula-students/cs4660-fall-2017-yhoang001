"""
Searches module defines all different search algorithms
"""
from queue import Queue
from graph import graph as gra
def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    actions = []
    # N = (None, None)
    q = Queue()
    q.put(initial_node)

    while (q.qsize() > 0):
        i = q.get()
        for node in graph.neighbors(i):
            if not hasattr(node, 'parent'):
                node.parent = i
            if node == dest_node:
                N = node
                while (N[1] is not None):
                    actions.append(gra.Edge(N.parent, N, graph.distance(N.parent, N)))
                    N = N.parent
                actions.reverse()
                return actions

            q.put(node)


def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    actions=[]
    for node in graph.neighbors(initial_node):
        if node == dest_node:
            return [graph.distance(initial_node, dest_node)]
        else:
            paths = dfs(graph, node, dest_node)
            # print(paths,'test')
            if paths != []:
                actions.append(graph.distance(initial_node, node))
                actions.extend(paths)
                return actions

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass
