import math
import numpy as np


class Bound:
    def __init__(self, tree):
        self.tree = tree
        self.lower_bound = None
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
            time = section.time
            clock += time

            # We change section
            id_start = section.get_father().get_id()
            section = self.tree.find_node(id_start).get_father()

        return clock + time_to_evacuate

    def calculate_lower_bound(self):
        lower_bound_per_evac_node = []
        for id_evac_node in self.tree.evac_node_id_list:
            lower_bound_per_evac_node.append(self.get_lower_bound_for_one_evac_node(id_evac_node))
        return max(lower_bound_per_evac_node)

    def calculate_upper_bound(self):
        time_limit = 1000
        data = self.tree
        time_list = []

        # Compute the min time for each evac node
        for node_id in data.evac_node_id_list:
            time = self.get_lower_bound_for_one_evac_node(node_id)
            time_list.append((node_id, time))

        # Order the list by time
        time_list = sorted(time_list, key=lambda evac: evac[2], reverse=True)

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
                index_arc = arc_list.index((father.father, father.son))
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
                index_arc = arc_list.index((father.father, father.son))
                interval += father.evac[node_id]
                entire_gp_nb = node.population//node.max_rate
                beg = t_min_current + interval
                end = t_min_current+entire_gp_nb
                for t in range(beg, end):
                    gantt[index_arc][t] += node.max_rate

                rest = node.population % node.max_rate
                if rest != 0:
                    gantt[index_arc][end] += rest
                    end += 1

                if t_max < end:
                    t_max = end

            node.chosen_rate = node.max_rate
            node.chosen_start_date = t_min_current
