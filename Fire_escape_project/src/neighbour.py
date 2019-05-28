from reader import *

class Neighbour:

    def __init__(self, solution):
        self.solution = solution

    def local_search_with_a_critical_node(self):

        finished = 0
        cpt = 0
        while not finished and cpt <20:
            cpt += 1
            print(self.solution.evac_nodes)
            # Find the most constraint node
            node_critical, id_max = self.find_critical_evac(self.solution.evac_nodes)

            # Change Max_rate
            node_rate, max_end_rate = self.change_parameter(1, node_critical, id_max)

            # Change Start_date until not valid and stop at the state that is valid
            node, max_end_start = self.change_parameter(0, node_rate, id_max)

            # if max_end_rate == max_end_start:
            #     finished = 1
            #     self.solution.objective = max_end_rate

    def change_parameter(self, mode, node, id_max):  # mode : 0 : start date / 1 : max rate

        old_node = node
        is_valid, max_end = self.solution.check_solution()
        max_end_old = None

        # Change Start_date until not valid and stop at the state that is valid
        while is_valid and (max_end !=max_end_old or max_end_old is None):
            is_valid_old, max_end_old = is_valid, max_end
            old_node = node
            if mode:
                if node['start_date'] > 0:
                    node["start_date"] -= 1
            else:
                if node["evac_rate"] > 0 and node["evac_rate"] < self.solution.data.nodes[id_max].max_rate :
                    node["evac_rate"] +=1
            self.solution.evac_nodes.update({id_max : node})
            is_valid, max_end = self.solution.check_solution()

        node = old_node
        max_end = max_end_old
        self.solution.evac_nodes.update({id_max : node})
        self.solution.objective = max_end
        return node, max_end

    # Return the evac node id for which the evacuation is the last to terminate
    # according the evacuation info given in parameter
    def find_critical_evac(self, evac_nodes):
        max_evac = None
        max_end = 0
        id_max = None
        for evac_node_id, value in evac_nodes.items():
            end = self.calculate_end_evac(evac_node_id, value['evac_rate'], value['start_date'])
            if max_end < end:
                max_end = end
                max_evac = evac_nodes[evac_node_id]
                id_max = evac_node_id
        return max_evac, id_max

    # Calculate the end time of the evacuation for the given evac node
    # warning : this function does not verify if an arc capacity is exceeded
    def calculate_end_evac(self, evac_node_id, evac_rate, start_date):
        evac_node = self.solution.data.nodes[evac_node_id]
        father_arc = evac_node.arc_father
        node_father = father_arc.father
        id_father = node_father.id_node

        while id_father != self.solution.data.safe_node_id:
            father_arc = node_father.arc_father
            node_father = father_arc.father
            id_father = node_father.id_node

        interval = father_arc.evac[evac_node_id] # interval between the evac node and the safe node
        end = start_date + interval + math.ceil(evac_node.population / evac_rate)

        return end


if __name__ == '__main__':
    bound = Bound(Reader("TD.txt").data)
    bound.calculate_upper_bound()
    bound.upper_bound
    neighbour = Neighbour(bound.upper_bound)
    neighbour.local_search_with_a_critical_node()
    print(neighbour.solution.write_solution("sol_neighbour"))



