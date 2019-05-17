
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

        time_to_evacuate = int(population / max_rate)

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
        pass
