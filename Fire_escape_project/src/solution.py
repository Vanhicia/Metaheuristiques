from reader import *
import numpy as np
import math


class Solution:

    def __init__(self, filename=None, data=None, evac_nodes=None, is_valid=None, objective=None, timestamp=None, method=None, other=None):
        self.filename = filename
        self.data = data
        self.evac_nodes = evac_nodes  # dictionary for the evac nodes (key = id, info = evac_rate & start_date)
        self.is_valid = is_valid
        self.objective = objective
        self.timestamp = timestamp
        self.method = method
        self.other = other

    # Check if the solution is valid
    # Return true and the objective if the solution is valid
    # Return false and -1 if not
    def check_solution(self, display=False):
        time_limit = 10000
        if self.data is None:
            self.data = Reader(self.filename).data
        arc_nb = len(self.data.arcs)
        max_end = 0  # To calculate the objective function

        # Matrix which represents the Gantt diagram
        # Each coefficient of the matrix represents the flow at the arc beginning
        gantt = np.zeros((arc_nb, time_limit))

        k = 0  # represents the arc index in the matrix
        # For each arc
        for arc in self.data.arcs.values():

            # For each evacuation crossing this arc
            for id1, interval in arc.evac.items():
                evac_node = self.data.nodes[id1]
                evac_info = self.evac_nodes[id1]

                beg = evac_info['start_date'] + interval
                end = int(beg + (evac_node.population//evac_info['evac_rate']))

                # Add the flow (of entire groups) in Gantt diagram (from beg to end-1)
                for i in range(beg, end):
                    gantt[k][i] += evac_info['evac_rate']

                # Add the flow of the last incomplete group if it exists
                rest = evac_node.population % evac_info['evac_rate']
                if rest != 0:
                    gantt[k][end] += rest
                    # Add 1 to the end date because it is the next interval
                    # (when the group has finished to cross the arc)
                    end += 1

                # Verify if the objective function has to be increased
                if max_end < (end + arc.length):
                    max_end = end + arc.length

            # Check the capacity is not exceeded
            for i in range(time_limit):
                # If the solution is not valid
                if arc.capacity < gantt[k][i]:
                    if display:
                        print("The solution is not valid !")
                    return False, -1

            k += 1

        if display:
            print("The solution is valid")
        # If the solution is valid, check the objective function
        if self.objective is not None:
            # if self.objective == max_end:
                if display:
                    print("Objective : " + str(max_end))
            # else:
            #     print("The objective is wrong : it is " + str(max_end) +", instead of " + str(self.objective))

        return True, max_end

    def read_solution(self, solution_file):

        # Open the file
        data_folder = Path("../solutions/")
        file_to_open = data_folder / solution_file

        with open(file_to_open, "r") as f:

            self.filename = f.readline().rstrip('\n\r') + ".txt"
            evac_node_nb = int(f.readline())
            self.evac_nodes = {}

            # Evac node information
            for k in range(evac_node_nb):
                id1, evac_rate, start_date = map(int, f.readline().rstrip('\n\r').split(" "))
                self.evac_nodes[id1] = {"evac_rate": evac_rate, "start_date": start_date}

            valid = f.readline().rstrip('\n\r')
            if valid == "valid":
                self.is_valid = True
            elif valid == "invalid":
                self.is_valid = False
            else:
                raise SyntaxError

            self.objective = int(f.readline())

    def write_solution(self, solution_filename):
        data_folder = Path("../solutions/")
        file_name = solution_filename + ".txt"
        file = open(data_folder / file_name, "w+")
        file.write(self.filename.rstrip(".full") + "\n")  # Nom de l'instance résolue
        file.write(str(len(self.data.evac_node_id_list)) + "\n")  # <nombre de sommets à évacuer>
        for evac_node_id in self.data.evac_node_id_list:
            # pour chaque sommet à évacuer :
            # <son identifiant>, <son taux d’évacuation>, <sa date de début d’évacuation>
            file.write(str(evac_node_id) + " " + str(self.evac_nodes[evac_node_id]['evac_rate']) + " " + str(self.evac_nodes[evac_node_id]['start_date']) + "\n")

        # nature de la solution : <valid ou invalid>
        if self.is_valid:
            file.write("valid\n")
        else:
            file.write("invalid\n")

        file.write(str(self.objective) + "\n")  # <valeur de la fonction objectif>

        file.write(str(self.timestamp) + "\n")   # <temps de calcul>

        # <méthode> : le nom de la méthode utilisée et la version de l’implémentation
        file.write(self.method + "\n")

        # champ libre (paramètre de la méthode, nom du binôme, ....)
        file.write(self.other)


if __name__ == '__main__':
    solution = Solution()
    solution.read_solution("solution_TD_non_opti.txt")
    print(solution.check_solution())





