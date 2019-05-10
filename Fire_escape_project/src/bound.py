from data_structure import *


class Bound:
    def __init__(self, tree):
        self.tree = tree
        self.lower_bound = None
        self.upper_bound = None

    def calculate_lower_bound(self):
        lower_bound_per_evac_node = []
        for id_evac_node in self.tree.evac_node_id_list:
            period = 0
            id_start = id_evac_node
            node_start = self.tree.find_node(id_evac_node)
            population = node_start.get_population()
            arrived_population = 0
            arc_father = node_start.get_father()
            cpt = 0
            while id_start != self.tree.safe_node_id and cpt < 20:
                cpt += 1
                time = arc_father.get_time()
                print("capacity")
                capacity = arc_father.get_capacity()
                while period < time:
                    if population > 0:
                        population -= capacity
                        arrived_population += capacity
                        print(population)
                    period += 1
                if population <= 0:
                    population = arrived_population
                    id_start = arc_father.get_father().get_id()
                    arc_father = self.tree.find_node(id_start).get_father()

            lower_bound_per_evac_node.append(period)
        return max(lower_bound_per_evac_node)

    def calculate_upper_bound(self):
        pass
