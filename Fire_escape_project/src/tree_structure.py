class Node:
    """ A Node is defined by
    - its id
    - its father (a node)
    - a list of edges which lead to its sons)
    """

    def __init__(self, id1):
        self.id=id1
        self.father=None
        self.sons=[]

    def __init__(self, id1, father):
        self.id = id1
        self.father=father
        self.sons=[]

    def add_edge(self, edge):
        self.sons.append(edge)

    def set_father(self, father):
        self.father=father


class EvacNode(Node):
    """An EvacNode is a Node with
    - a population
    - a max rate
    """
    def __init__(self, id1, population, max_rate):
        Node.__init__(self, id1)
        self.population=population
        self.max_rate=max_rate

class Edge:
    """ An Edge is defined by
    - two Nodes (the father and the son)
    - due date
    - length
    - capacity
    """

    def __init__(self, father, son):
        self.father = father
        self.son = son
        self.due_date = -1
        self.length = -1
        self.capacity = -1

     def __init__(self, father, son, due_date, length, capacity):
         self.father=father
         self.son= son
         self.due_date=due_date
         self.length=length
         self.capacity=capacity

    def add_info(self, due_date, length, capacity):
         self.due_date=due_date
         self.length=length
         self.capacity=capacity


class Tree:
    """A Tree is defined by
        - its root (node)
        """

    def __init__(self, node):
        self.root=node


    def find_edge(self, node1, node2):
        #TODO

    def node_exist(self, node1):
        node = self.root
        #TODO

