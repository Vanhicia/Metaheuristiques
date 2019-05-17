class Data:
    """ Attributes:
        - nodes : a dictionary of nodes
        - arcs: a dictionary of arcs
        - safe_node_id : the id of the safe node
        - evac_node_id_list : the list of evac node ids
    """

    def __init__(self, id1):
        self.nodes = {}
        self.arcs = {}
        self.safe_node_id = id1
        self.evac_node_id_list = []

    def get_nodes(self):
        return self.nodes

    def get_arcs(self):
        return self.arcs

    def get_safe_node_id(self):
        return self.safe_node_id

    def get_evac_node_id_list(self):
        return self.evac_node_id_list

    # Add the node if it doesn't exist yet
    def add_node(self, id1):
        self.nodes.setdefault(id1, Node(id1))

    # Add the node if it doesn't exist yet
    def add_evac_node(self, id1, population, max_rate):
        self.nodes.setdefault(id1, EvacNode(id1, population, max_rate))
        self.evac_node_id_list.append(id1)

    # Add the arc if it doesn't exist yet but the two nodes exist
    # And add the evac node (which uses this arc) in the structure of the arc
    def add_arc(self, father_id, son_id, evac_node_id):
        try:
            # Check both nodes exist
            _node1 = self.nodes[father_id]
            _node2 = self.nodes[son_id]
            # Create the arc if it doesn't exist
            self.arcs.setdefault((father_id, son_id), Arc(self, father_id, son_id))
            # Add the evac node which uses the arc
            self.arcs[(father_id, son_id)].add_evac(evac_node_id)
        except KeyError:
            print("add_arc: This arc can't be added")

    # Add information about the arc between the nodes id1 and id2
    # The order of the nodes doesn't matter
    def add_arc_info(self, id1, id2, due_date, length, capacity):
        # Look for the arc
        try:
            arc = self.arcs[(id1, id2)]
            # Add information about the arc
            arc.add_info(due_date, length, capacity)
        except KeyError:
            try:
                arc = self.arcs[(id2, id1)]
                # Add information about the arc
                arc.add_info(due_date, length, capacity)
            except KeyError:
                pass
                # The arc has not been found, it is certainly a useless arc
                # So we do nothing
                # print("add_arc_info: not info add because the arc doesn't exist")

    # Method called a the end of the creation if the tree
    # Update intervals between evac nodes and arcs
    def update_interval(self):
        for node in self.evac_node_id_list:
            interval = 0
            father = self.nodes[node].father
            while father is not None:
                father.add_interval_for_evac(node, interval)
                interval += father.time
                father = father.father.father

    # Return the node id1
    # Return None if it doesn't exist
    def find_node(self, id1):
        try:
            node = self.nodes[id1]
        except KeyError:
            node = None
            print("find_node: This Node has not been found")
        return node

    # Return the arc between the nodes id1 and id2
    # Return None if the arc doesn't exist
    def find_arc(self, id1, id2):
        try:
            arc = self.arcs[(id1, id2)]
        except KeyError:
            try:
                arc = self.arcs[(id2, id1)]
            except KeyError:
                arc = None
                print("find_arc : this arc has not been found !")
        return arc

    def print_tree(self):
        node = self.nodes[self.safe_node_id]
        node.print_tree()

    def print_dict_nodes(self):
        print("List of nodes :", end=' ')
        for key, _ in self.nodes.items():
            print(key, end=' ')
        print()

    def print_dict_arcs(self):
        print("List of arcs :", end=' ')
        for key, _ in self.arcs.items():
            print(key, end=' ')
        print()


class Node:
    """ A Node is defined by
    - id
    - father : the arc which leads to its father
    - sons : a list of arcs which lead to its sons
    """

    def __init__(self, id1):
        self.id1 = id1
        self.father = None
        self.sons = []

    def get_id(self):
        return self.id1

    def get_father(self):
        return self.father

    def get_sons(self):
        return self.sons

    def add_arc_successor(self, arc):
        self.sons.append(arc)

    def set_father(self, arc):
        if self.father is None:
            self.father = arc
        else:
            print("set_father: This node has already a father")

    # Return None if the Node doesn't have this son
    # Else return the arc between the current node and the indicated node
    def find_arc_successor(self, node_id):
        arc = None
        k = 0
        n = len(self.sons)
        while arc is None and k < n:
            arc_son = self.sons[k]
            if arc_son.son.id1 == node_id:
                arc = self.sons[k]
            k += 1
        return arc

    # Print the tree in the console
    def print_tree(self, k=0):
        deb = ""

        for i in range(k):
            deb += "        "

        deb += str(self.id1) + " -> "

        # Print the sons of the node
        for son in self.sons:
            print(deb + str(son.get_son().id1))

        # Recursion
        k += 1
        for son in self.sons:
            son.get_son().print_tree(k)


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
    - two Node (the father and the son)
    - due date
    - time
    - capacity
    - evac : a dictionary for the evacuations using this arc (key = node id, info = interval)
    """

    def __init__(self, data, father_id, son_id, due_date=-1, time=-1, capacity=-1):
        self.father = data.nodes[father_id]
        self.son = data.nodes[son_id]
        self.due_date = due_date
        self.time = time
        self.capacity = capacity
        self.evac = {}

        # Add the arc in the structure of both implied nodes if it doesn't exist
        if self.father.find_arc_successor(son_id) is None:
            self.father.add_arc_successor(self)
            self.son.set_father(self)

    def add_info(self, due_date, time, capacity):
        self.due_date = due_date
        self.time = time
        self.capacity = capacity

    def add_evac(self, id1):
        self.evac[id1] = 0

    def add_interval_for_evac(self, id1, time):
        self.evac[id1] = time

    def get_father(self):
        return self.father

    def get_son(self):
        return self.son

    def get_due_date(self):
        return self.due_date

    def get_time(self):
        return self.time

    def get_capacity(self):
        return self.capacity


class SolutionEvacNode(EvacNode):

    def __init__(self, id1, rate, start_date):
        Node.__init__(self, id1)
        self.chosen_rate = rate
        self.chosen_start_date = start_date


# Test
#
# if __name__ == '__main__':
#     data = Data(0)
#     data.add_node(0)
#     data.add_node(1)
#     data.add_node(2)
#     data.add_evac_node(3, 10, 5)
#     data.add_evac_node(4, 8, 2)
#     data.add_evac_node(5, 6, 3)
#
#     data.add_arc(0, 1)
#     data.add_arc(0, 2)
#     data.add_arc(1, 3)
#     data.add_arc(1, 4)
#     data.add_arc(2, 5)
#
#     data.print_tree()


