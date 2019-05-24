import math
import numpy as np
import time
from solution import *
from reader import *

class Bound:

    def __init__(self, tree):
        self.tree = tree
        self.lower_bound = None
        self.timestamp_lower_bound = None
        self.upper_bound = None

    def get_lower_bound_for_one_evac_node(self, id_evac_node):
        clock = 0

        # We get information on where to start
        id_start = id_evac_node
        node_start = self.tree.find_node(id_evac_node)
        section = node_start.father

        population = node_start.population
        max_rate = node_start.max_rate

        time_to_evacuate = math.ceil(population / max_rate)

        while id_start != self.tree.safe_node_id:
            # We get the time of the current section and add it
            time_section = section.time
            clock += time_section

            # We change section
            id_start = section.get_father().get_id()
            section = self.tree.find_node(id_start).get_father()
        return clock + time_to_evacuate

    def calculate_lower_bound(self):
        lower_bound_per_evac_node = []
        start = time.time()
        for id_evac_node in self.tree.evac_node_id_list:
            lower_bound_per_evac_node.append(self.get_lower_bound_for_one_evac_node(id_evac_node))
        end = time.time()
        self.lower_bound = max(lower_bound_per_evac_node)
        self.timestamp_lower_bound = end - start

    def calculate_upper_bound(self):
        time_limit = 1000
        data = self.tree
        time_list = []
        evac_nodes_dict = {}
        objective = 0

        start_prog = time.time()

        # Compute the min time for each evac node
        for node_id in data.evac_node_id_list:
            time_one_node = self.get_lower_bound_for_one_evac_node(node_id)
            time_list.append((node_id, time_one_node))

        # Order the list by time
        time_list = sorted(time_list, key=lambda evac: evac[1], reverse=True)

        t_min = 0
        t_max = 0
        gantt = np.zeros((len(data.arcs), time_limit))

        # Create an arc list in order to link the indexes of line matrix with arcs
        arc_list = []
        for key in data.arcs.keys():
            arc_list.append(key)

        for node_id, evac_time in time_list:
            node = data.nodes[node_id]
            father = node.father
            t_min_current = t_min
            interval = 0

            # look for the start date #

            # for each arc of the evacuation road
            while father is not None:
                index_arc = arc_list.index((father.father.id1, father.son.id1))
                interval += father.evac[node_id]

                # look for the date when the not used capacity is enough
                for t in range(t_min_current + interval, t_max):
                    if (father.capacity-gantt[index_arc][t]) < node.max_rate:
                        t_min_current = t - interval

                # take the next arc of the road evacuation
                father = father.father.father

            # add the flow for the evaluated evacuation node #
            # with rate = max_rate and start time = t_min_current
            father = node.father
            interval = 0
            # for each arc of the evacuation road
            while father is not None:
                is_max = False
                index_arc = arc_list.index((father.father.id1, father.son.id1))
                interval += father.evac[node_id]
                entire_gp_nb = node.population//node.max_rate
                beg = t_min_current + interval
                end = beg + entire_gp_nb

                if objective < (end + father.time):
                    is_max = True
                    objective = end + father.time

                for t in range(beg, end):
                    gantt[index_arc][t] += node.max_rate

                rest = node.population % node.max_rate
                if rest != 0:
                    gantt[index_arc][end] += rest
                    end += 1
                    if is_max:
                        objective += 1

                if t_max < end:
                    t_max = end

                # take the next arc of the road evacuation
                father = father.father.father

            evac_nodes_dict[node_id] = {"evac_rate": node.max_rate, "start_date": t_min_current}

        end_prog = time.time()
        timestamp = end_prog - start_prog

        self.upper_bound = Solution(data.filename, data, evac_nodes_dict, True, objective, timestamp, "Upper bound", "Kim-Anh & Alicia")


if __name__ == '__main__':
    read = Reader("TD.txt")
    bound = Bound(read.data)
    bound.calculate_upper_bound()
    print("objective of the upper bound for the TD instance:")
    print(bound.upper_bound.objective)
    bound.upper_bound.check_solution()
    #bound.upper_bound.write_solution("solution_TD_upper_bound")