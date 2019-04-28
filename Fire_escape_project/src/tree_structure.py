class Node:
    """ A Node is defined by
    - its id
    - its father (a node)
    - a list of arcs which lead to its sons)
    """

    def __init__(self, id1):
        self.id = id1
        self.father = None
        self.sons = []

    def get_id(self):
        return self.id

    def get_father(self):
        return self.father

    def get_sons(self):
        return self.sons

    def get_son_nb(self):
        return len(self.sons)

   """ def __add_arc_successor(self, arc):
        self.sons.append(arc)

    def __set_father(self, father):
        self.father = father"""

    # Return None if the Node doesn't have this son
    # Else return the arc between the current node and the indicated node
    def find_arc_successor(self, node_id):
        arc = None
        k = 0
        n = len(self.sons)
        while arc.equals(None) and k < n:
            node = self.sons[k]
            if node.id == node_id:
                arc = self.sons[k]
            k += 1
        return arc

    def add_arc(self, arc):

        # TODO

    """ Methods for trees """

    # Return None if not found
    # Return the arc if it is found in the tree
    def find_arc(self, node1_id, node2_id):
        arc = None
        # If the current node is node1
        if self.id == node1_id:
            arc = self.find_arc_successor(node2_id)
        # If the current node is node2
        elif self.id == node2_id:
            arc = self.find_arc_successor(node1_id)
        # Else, recursion with its sons
        else:
            k = 0
            n = len(self.sons)
            while arc.equals(None) and k < n:
                arc = self.sons[k].find_arc(node1_id, node2_id)
                k += 1
        return arc


    # Have one id and check if the tree contains a node with this id
    # Return a boolean (True or False)
    def node_exists(self, node_id):
        found = False
        # If the current node is the wanted node
        if self.id == node_id:
            found = True
        # Else, recursion with its sons
        else:
            k = 0
            n = len(self.sons)
            while node.equals(None) and k < n:
                found = self.has_descendant(node_id)
                k += 1
        return found


    # Return the node which has the given id
    def get_node_by_id(self, node_id):
        node = None
        # If the current node is the wanted node
        if self.id == node_id:
            node = self
        # Else, recursion with its sons
        else:
            k = 0
            n = len(self.sons)
            while node.equals(None) and k < n:
                node = self.get_node_by_id(node_id)
        return node

    # Print the tree in the console
    def print_tree(self):

    # TODO


class EvacNode(Node):
    """An EvacNode is a Node with
    - a population
    - a max rate
    """

    def __init__(self, id1, population, max_rate):
        Node.__init__(self, id1)
        self.population = population
        self.max_rate = max_rate

    def get_population(self):
        return self.population

    def get_max_rate(self):
        return self.max_rate


class Arc:
    """ An Arc is defined by
    - two Nodes (the father and the son)
    - due date
    - length
    - capacity
    """

    def __init__(self, father, son, due_date=-1, length=-1, capacity=-1):
         self.father = father
         self.son = son
         self.due_date = due_date
         self.length = length
         self.capacity = capacity

    def add_info(self, due_date, length, capacity):
         self.due_date = due_date
         self.length = length
         self.capacity = capacity

    def get_father(self):
        return self.father

    def get_son(self):
        return self.son

    def get_due_date(self):
        return self.due_date

    def get_length(self):
        return self.length

    def get_capacity(self):
        return self.capacity

"""
class Tree():
    A Tree is defined by
        - its root (node)
    

    def __init__(self, node):
        self.root = node

    
        
"""


if __name__ == '__main__':
    n0 = Node(0)
    n1 = Node(1,0)
    n2 = Node(2,0)
    n3 = Node(3,1)
    n4 = Node(4,1)
    n5 = Node(5,2)

