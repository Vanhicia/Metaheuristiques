from pathlib import Path
from data_structure import *


class Reader:

    def __init__(self, path):
        self.path = path  # Path containing the name of a file (string)
        self.data = get_data_from_file(path)  # Generated Tree from the file


#  Read a file and return the associated tree
def get_data_from_file(path):

    # Open the file
    data_folder = Path("../instances/")
    file_to_open = data_folder / path
    f = open(file_to_open, "r")

    line = f.readline()
    count = 1  # counter for changing line
    info = 0  # 0 : we are not in a section / 1: we are in evacuation info section / 2: we are in graph info section
    header = 0  # 0 : we are not on the header / 1: we are on the header of a section (Evacuation info, Graph info)
    data = None

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
                    data = Data(id_safe_node)
                else:  # We are on a definition of an evac_node (line)
                    treat_one_evac_node(line, data)

            # Graph info
            elif info == 2:
                if header == 1:  # We are on the header: <num nodes> <num edges>
                    header = 0
                else:  # We are on a definition of an edge (line): <node 1> <node 2> <due date> <length> <capacity>
                    [node1_id, node2_id, due_date, length, capacity] = line.split(" ")
                    data.add_arc_info(node1_id, node2_id, due_date, length, capacity)

            else:
                raise Exception("Error : We are not in a section such as Evacuation info or Graph info.")
        count += 1
    return data


#  We add the path from the evac_node to the safe node
def treat_one_evac_node(line, data):
    evac_node_info = line.split(" ")  # We get all information of the evac node

    id_evac_node = evac_node_info[0]  # id of evac_node
    population = evac_node_info[1]  # population of evac node
    max_rate = evac_node_info[2]  # max rate of evac node
    k = evac_node_info[3]  # number of parts in the evacuation route

    data.add_evac_node(id_evac_node, population, max_rate)  # We create the evac node with its information

    id_son = id_evac_node

    for i in range(0, k):
        id_father = evac_node_info[4 + i]

        data.add_node(id_father) # The node is added only if it doesn't exist yet

        data.add_arc(id_father, id_son) # The arc is added only if it doesn't exist yet

        id_son = id_father


# Tests unitaires
# data_folder = Path("../instances/")
# file_to_open = data_folder / "dense_10_30_3_1.full"
# read_file(file_to_open)

# read = Reader("dense_10_30_3_1.full")
# print_tree(read.tree)

