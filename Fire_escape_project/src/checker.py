from pathlib import Path
from data_structure import *
from reader import *
import numpy as np


class Checker:
    """ Attributes:
    - instance : file name of the instance
    - evac_nodes : dictionary for the evac nodes (key = id, info = evac_rate & start_date)
    - valid : true if the solution is valid
    - objective : value of the objective function
    """

    def __init__(self, path):

        # Open the file
        data_folder = Path("../solutions/")
        file_to_open = data_folder / path

        with open(file_to_open, "r") as f:

            self.instance = f.readline().rstrip('\n\r')+".txt"
            evac_node_nb = int(f.readline())
            self.evac_nodes = {}

            # Evac node information
            for k in range(evac_node_nb):
                id1, evac_rate, start_date = map(int, f.readline().rstrip('\n\r').split(" "))
                self.evac_nodes[id1] = {"evac_rate": evac_rate, "start_date": start_date}

            valid = f.readline().rstrip('\n\r')
            if valid == "valid":
                self.valid = True
            elif valid == "invalid":
                self.valid = False
            else:
                raise SyntaxError

            self.objective = int(f.readline())

    def check_solution(self):
        time_limit = 1000
        reader = Reader(self.instance)
        data = reader.data
        arc_nb = len(data.arcs)
        max_end = 0

        guant = np.zeros((arc_nb, time_limit))

        k = 0
        for arc in data.arcs.values():
            print("loop arc")
            print("father = "+str(arc.father.id1))
            print("son = "+str(arc.son.id1))

            for id1, interval in arc.evac.items():
                is_max = False
                evac_node = data.nodes[id1]
                evac_info = self.evac_nodes[id1]

                beg = evac_info['start_date'] + interval
                end = int(beg + (evac_node.population//evac_info['evac_rate']))

                if max_end < (end + arc.time):
                    is_max = True
                    max_end = end + arc.time

                print("id evac node = " + str(id1))
                print("beg = " + str(beg))
                print("end = " + str(end))
                print("rate = " + str(evac_info['evac_rate']))

                for i in range(beg, end):
                    guant[k][i] += evac_info['evac_rate']

                rest = evac_node.population % evac_info['evac_rate']
                if rest != 0:
                    guant[k][end] += rest
                    if is_max:
                        max_end += 1

            # Check the capacity is not exceeded
            for i in range(time_limit):
                # If the solution is not valid
                if arc.capacity < guant[k][i]:
                    if not self.valid:
                        return True
                    else:
                        return False

            k += 1

        print("The solution is valid")
        if self.objective == max_end:
            print("Objective : " + str(max_end))
        else:
            print("The objective is wrong : it is %d, instead of %d", max_end, self.objective)

        return True


if __name__ == '__main__':
    checker = Checker("solution_TD_non_opti.txt")
    print(checker.check_solution())
