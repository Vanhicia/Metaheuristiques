class Node:
    """ A Node is defined by
    - its father (a node)
    - a list of edges which lead to its sons)
    """

    def __init__(self):
        self._father=None
        self._sons=[]

    def __init__(self, father):
        self._father=father
        self._sons=[]

    def add_edge(self, edge):
        self._sons.append(edge)


class EvacNode(Node):
    """An EvacNode is a Node with
    - a population
    - a max rate
    """
    def __init__(self, population):
        Node.__init__(self)
        self._population=population

class Edge:
    """ An Edge is defined by
    - two Nodes (the father and the son)
    - due date
    - length
    - capacity
    """
     def _init__(self, father, son, due_date, length, capacity):
         self._father=father
         self._son= son
         self._due_date=due_date
         self._length=length
         self._capacity=capacity


class Tree:
    """A Tree is defined by
        - its root (node)
        """

    def __init__(self, node):
        self._root=node