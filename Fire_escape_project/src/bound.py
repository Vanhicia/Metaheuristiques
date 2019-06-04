import math
import numpy as np
import time
from reader import *
from solution import *
from random import shuffle
import collections


class Bound:

    def __init__(self, data):
        self.data = data
        self.lower_bound = None
        self.upper_bound = None

    def get_block_time_for_one_evac_node(self, id_evac_node):
        clock = 0

        # We get information on where to start
        id_start = id_evac_node
        node_start = self.data.nodes[id_evac_node]
        section = node_start.arc_father

        population = node_start.population
        max_rate = self.find_min_capacity(id_evac_node, self.data.safe_node_id)

        time_to_evacuate = math.ceil(population / max_rate)

        while id_start != self.data.safe_node_id:
            # We get the time of the current section and add it
            time_section = section.length
            clock += time_section

            # We change section
            id_start = (section.father).id_node
            section = self.data.find_node(id_start).arc_father
        return clock + time_to_evacuate

    def calculate_lower_bound(self):
        start = time.time()

        lower_bound_per_evac_node = []
        evac_nodes_dict = {}
        data = self.data

        # Add lower bound of all evac nodes in a list and a dictionary
        for id_evac_node in data.evac_node_id_list:
            lower_bound_per_evac_node.append(self.get_block_time_for_one_evac_node(id_evac_node))
            evac_nodes_dict[id_evac_node] = {"evac_rate": data.nodes[id_evac_node].max_rate,
                                             "start_date": 0}

        end = time.time()
        timestamp = end - start
        self.lower_bound = Solution(data.filename, data, evac_nodes_dict, False, max(lower_bound_per_evac_node),
                                    timestamp, "Lower bound", "Kim-Anh & Alicia")

    def calculate_upper_bound(self, random=False):
        start_prog = time.time()

        data = self.data
        time_list = []
        evac_nodes_dict = {}
        objective = 0
        max_time = 0
        block_time_per_evac_nodes = {}

        for id_evac_node in data.evac_node_id_list:
            data.nodes[id_evac_node].max_rate = self.find_min_capacity(id_evac_node, data.safe_node_id)
            start_date = self.determine_latest_start(id_evac_node, data.safe_node_id)
            section = data.nodes[id_evac_node].arc_father

            block_time_per_evac_nodes[id_evac_node] = {'block_time': self.get_block_time_for_one_evac_node(id_evac_node),
                                                       'first_due_date': section.due_date,
                                                       'latest_start_date': start_date}

        # Order list by first_due_date, then latest_start_date
        time_list = sorted(block_time_per_evac_nodes.items(),
                           key = lambda kv: (kv[1]['first_due_date'],
                                             kv[1]['latest_start_date']),
                           )
        if random:
            shuffle(time_list)

        time_limit = 10000

        t_min = 0
        t_max = 0
        gantt = np.zeros((len(data.arcs), time_limit))

        # Create an arc list in order to link the indexes of line matrix with arcs
        arc_list = list(data.arcs.keys())

        for node_id, val in time_list:
            node = data.nodes[node_id]
            arc_father = node.arc_father
            node.max_rate = node.max_rate
            t_min_current = t_min

            # look for the start date #
            # for each arc of the evacuation road
            while arc_father is not None:
                index_arc = arc_list.index((arc_father.father.id_node, arc_father.son.id_node))
                interval = arc_father.evac[node_id]

                # look for the date when the not used capacity is enough
                for t in range(t_min_current + interval, t_max+1):

                    if arc_father.capacity < (gantt[index_arc][t] + node.max_rate):
                        t_min_current = (t+1) - interval

                # take the next arc of the road evacuation
                arc_father = arc_father.father.arc_father

            # add the flow for the evaluated evacuation node #
            # with rate = max_rate and start time = t_min_current
            arc_father = node.arc_father

            # for each arc of the evacuation road
            while arc_father is not None:
                is_max = False
                index_arc = arc_list.index((arc_father.father.id_node, arc_father.son.id_node))
                interval = arc_father.evac[node_id]
                entire_gp_nb = node.population//node.max_rate
                beg = t_min_current + interval
                end = beg + entire_gp_nb

                for t in range(beg, end):
                    gantt[index_arc][t] += node.max_rate
                    if gantt[index_arc][t] > arc_father.capacity:
                        print("Erreur capa !!!!!!!!")

                rest = node.population % node.max_rate
                if rest != 0:
                    gantt[index_arc][end] += rest
                    end += 1

                if objective < (end + arc_father.length):
                    objective = end + arc_father.length

                if t_max < end:
                    t_max = end

                # take the next arc of the road evacuation
                arc_father = arc_father.father.arc_father

            evac_nodes_dict[node_id] = {"evac_rate": node.max_rate, "start_date": t_min_current}

        end_prog = time.time()
        timestamp = end_prog - start_prog

        self.upper_bound = Solution(data.filename, data, evac_nodes_dict, True, objective, timestamp, "Upper bound", "Kim-Anh & Alicia")

    # Return the min rate that we can evacuate
    def find_min_capacity(self, id_evac_node, safe_node_id):

        id_node_current = id_evac_node
        min_rate = self.data.nodes[id_evac_node].max_rate
        section =  self.data.nodes[id_evac_node].arc_father

        while id_node_current != safe_node_id:
            if section.capacity < min_rate:
                min_rate = section.capacity

            id_node_current = (section.father).id_node
            section = self.data.find_node(id_node_current).arc_father
        return min_rate

    def determine_latest_start(self, id_evac_node, safe_node_id):
        path = []
        id_node_current = id_evac_node
        section =  self.data.nodes[id_evac_node].arc_father

        while id_node_current != safe_node_id:
            path.append(section)
            id_node_current = (section.father).id_node
            section = self.data.find_node(id_node_current).arc_father

        path.reverse()
        start = path[0].due_date
        last = path[len(path)-1]
        for arc in path:
            start -= arc.length
            if arc.due_date < start:
                start = arc.due_date
        return start


if __name__ == '__main__':

    # --------- INPUTS ---------  #
    # filename = "TD"
    # filename = "ExempleSimple"
    # filename = "dense_10_30_3_1_I"
    # filename = "dense_10_30_3_3_I"
    filename = "dense_10_30_3_2_I"
    # read = Reader(filename +".txt")
    read = Reader(filename + ".full")
    bound = Bound(read.data)

    # ------ LOWER BOUND -------  #
    bound.calculate_lower_bound()
    print("objective of the lower bound for the " + filename + " instance:")
    print(bound.lower_bound.objective)
    bound.lower_bound.check_solution()
    bound.lower_bound.write_solution("solution_" + filename + "_lower_bound")

    # ------ UPPER BOUND -------  #
    bound.calculate_upper_bound()
    print("objective of the upper bound for the " + filename + " instance:")
    print(bound.upper_bound.objective)
    bound.upper_bound.check_solution()
    bound.upper_bound.write_solution("solution_" + filename + "_upper_bound")

