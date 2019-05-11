import math


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
        arrived_population = 0
        size_package_at_start = 0

        start = 1
        coef = 1

        while id_start != self.tree.safe_node_id:

            # We get information of the current section
            time = section.time
            capacity = section.capacity

            period = 0

            while period < time:
                if population > 0:
                    # We get the number of people we can evacuate for one clock
                    if start:
                        size_package_at_start += capacity
                        start = 0

                    coef = int(capacity/size_package_at_start)

                    # If the capacity's section is enough to put more people,
                    # we increase the number of people to evacuate for one clock
                    if coef > 1:
                        size_package_at_start *= coef

                    # If the capacity's section is too small,
                    # we decrease the number of people to evacuate for one clock
                    if size_package_at_start > capacity:
                        size_package_at_start = math.ceil(population/capacity)

                    population -= size_package_at_start
                    arrived_population += size_package_at_start

                # We count the time we are in this section
                period += 1

            clock += period

            if population <= 0:  # We arrived at the end of a section
                # We reinitialize population variable
                population = arrived_population
                arrived_population = 0
                # We change section
                id_start = section.get_father().get_id()
                section = self.tree.find_node(id_start).get_father()

        return clock + int(population/(coef*size_package_at_start))

    def calculate_lower_bound(self):
        lower_bound_per_evac_node = []
        for id_evac_node in self.tree.evac_node_id_list:
            lower_bound_per_evac_node.append(self.get_lower_bound_for_one_evac_node(id_evac_node))
        return max(lower_bound_per_evac_node)

    def calculate_upper_bound(self):
        pass
