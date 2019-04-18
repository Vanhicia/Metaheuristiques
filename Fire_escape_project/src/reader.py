from pathlib import Path
from tree_structure import *


class Reader:

    def __init__(self, path):
        self.path = path  # Path containing the name of a file (string)
        self.tree = get_tree_from_file(path)  # Generated Tree from the file


#  Read a file and return the associated tree
def get_tree_from_file(path):

    # Open the file
    data_folder = Path("../instances/")
    file_to_open = data_folder / path
    f = open(file_to_open, "r")

    line = f.readline()
    count = 1  # counter for changing line
    info = 0  # 0 : we are not in a section / 1: we are in evacuation info section / 2: we are in graph info section
    header = 0  # 0 : we are not on the header / 1: we are on the header of a section (Evacuation info, Graph info)
    tree = None

    while line:

        # We analyze Evacuation info
        if "c [evacuation info]" in line:
            info = 1
            header = 1
        #  We analyze Graph info
        elif "c [graph]" in line:
            info = 2
            header = 1

        else:
            # Evacuation info
            if info == 1:
                if header == 1:  # We are on the header: <num evac nodes> <id of safe node>
                    [_, id_safe_node] = line.split(" ")
                    header = 0
                    tree = Tree(Node(id_safe_node))
                else:  # We are on a definition of an evac_node (line)
                    treat_one_evac_node(line, tree)

            # Graph info
            elif info == 2:
                if header == 1:  # We are on the header: <num nodes> <num edges>
                    header = 0
                else:  # We are on a definition of an edge (line): <node 1> <node 2> <duedate> <length> <capacity>
                    [node1, node2, due_date, length, capacity] = line.split(" ")
                    update_one_edge_info(tree, node1, node2, due_date, length, capacity)

            else:
                raise Exception("Error : We are not in a section such as Evacuation info or Graph info.")
        count += 1
    return tree


#  We add the path from the evac_node to the safe node
def treat_one_evac_node(line, tree):
    evac_node_info = line.split(" ")  # We get all information of the evac node

    id_evac_node = evac_node_info[0]  # id of evac_node
    population = evac_node_info[1]  # population of evac node
    max_rate = evac_node_info[2]  # max rate of evac node
    k = evac_node_info[3]  # number of parts in the evacuation route

    evac_node = EvacNode(id_evac_node, population, max_rate)  # We create the evac node with its information

    son = evac_node

    for i in range(0, k):
        id_father = evac_node_info[4 + i]

        if not(tree.node_exist(id_father)):  # The parent node does not exist
            father = Node(id_father)  # We create it
        else:
            father = tree.get_node_by_id(id_father) # The parent node exists, we get it

        father.add_edge(Edge(father, son))  # We update its sons list
        son.set_father(father)  # We set the father for the son node
        son = father


def update_one_edge_info(tree, node1, node2, due_date, length, capacity):
    edge = tree.find_edge(node1, node2)
    if edge is not None:  # The edge exists
        edge.add_info(due_date, length, capacity)  # We update its info
    else:
        raise Exception("Error : The edge does not exist, we cannot update its information.")

# Tests unitaires
# data_folder = Path("../instances/")
# file_to_open = data_folder / "dense_10_30_3_1.full"
# read_file(file_to_open)

# read = Reader("dense_10_30_3_1.full")
# print_tree(read.tree)

