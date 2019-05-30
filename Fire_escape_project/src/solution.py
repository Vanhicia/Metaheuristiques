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

#     def add_info_in_gantt(self, gantt, id_evac_node, clock):
#         # We get information on where to start
#         id_start = id_evac_node
#         node_start = self.data.nodes[id_evac_node]
#         section = node_start.arc_father
#
#         population = node_start.population
#         arrived_population = 0
#         max_rate = node_start.max_rate
#         index_arc = list(self.data.arcs.keys()).index((section.father.id_node, section.son.id_node))
#         time_to_evacuate = math.ceil(population / max_rate)
#
#         while id_start != self.data.safe_node_id:
#             # We get the time of the current section and add it
#             time_section = section.time+clock
#             while time_section > clock:
# # gérer pb de capa et c'est bon
#                     clock += 1
#                     if gantt[index_arc][clock] == 0 :
#                         math.ceil(population / section.capacity)
#
#                         if section.capacity >= max_rate:
#                             if population - max_rate > 0:
#                                 arrived_population += max_rate
#                                 population -= max_rate
#                             else :
#                                 arrived_population += population
#                                 population = 0
#                             gantt[index_arc][clock] = arrived_population
#                         else:
#                             max_rate = section.capacity
#                             if population - max_rate > 0:
#                                 arrived_population += max_rate
#                                 population -= max_rate
#                             else :
#                                 arrived_population += population
#                                 population = 0
#                             gantt[index_arc][clock] = arrived_population
#
#
#             # We change section
#             id_start = (section.father).id_node
#             section = self.data.find_node(id_start).arc_father
#             if id_start != self.data.safe_node_id:
#                 index_arc = list(self.data.arcs.keys()).index((section.father.id_node, section.son.id_node))
#             population = arrived_population
#             arrived_population = 0
#
#         while time_to_evacuate > 0:
#             clock += 1
#             gantt[index_arc][clock] = -1
#             time_to_evacuate -= 1
#         return True, clock
#
#     def check_solution(self):
#         res = True
#         time_limit = 1000
#         list_bound_clock = []
#         if self.data is None:
#             self.data = Reader(self.filename).data
#
#         arc_nb = len(self.data.arcs)
#
#         gantt = np.zeros((arc_nb, time_limit))
#
#         for clock in range (time_limit):
#             for id_evac_node, value in self.evac_nodes.items():
#                 if value['start_date'] == clock:
#                     res, bound_clock = self.add_info_in_gantt(gantt, id_evac_node, clock)
#                     list_bound_clock.append(bound_clock)
#                 if not res :
#                     print("The solution is NOT valid")
#                     return False, -1
#         print("The solution is valid")
#         max_end = max(list_bound_clock)
#         if self.objective is not None:
#             print("Objective : " + str(max_end))
#         return True, max_end
#




    # Check if the solution is valid and in this case, if the objective is right
    # Return true and the objective if the solution is valid
    def check_solution(self):
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
                    print("The solution is not valid !")
                    return False, -1

            k += 1
        print("The solution is valid")
        # If the solution is valid, check the objective function
        if self.objective is not None:
            # if self.objective == max_end:
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





