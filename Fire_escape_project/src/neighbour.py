from reader import *


class Neighbour:

    def __init__(self, solution):
        self.solution = solution

    def local_search_with_a_critical_node(self):
        node_critical_old = None
        finished = 0
        while not finished:
            # Find the most constraint node
            node_critical_current, id_max = self.find_critical_evac(self.solution.evac_nodes)

            # Change Max_rate
            node_rate, max_end_rate, finished_rate = self.change_parameter(1, node_critical_current, id_max)

            # Change Start_date until not valid and stop at the state that is valid
            node, max_end_start, finished_date = self.change_parameter(0, node_rate, id_max)

            if finished_rate and finished_date and node_critical_current == node_critical_old:
                finished = 1

            node_critical_old = node_critical_current

    def change_parameter(self, mode, node, id_max):  # mode : 0 : start date / 1 : max rate
        finished = 0
        old_node = node.copy()

        is_valid, max_end = self.solution.check_solution()

        max_end_old = None

        # Change Start_date and Max_rate until that is not valid and stop at the state that is valid
        # or stop when we cannot change more
        while is_valid and not finished:
            if mode:
                # Change Start_date
                if node['start_date'] > 0:
                    node["start_date"] -= 1
                else:
                    finished = 1
            else:
                # Change Max_rate
                if 0 < node["evac_rate"] < self.solution.data.nodes[id_max].max_rate:
                    node["evac_rate"] += 1

                else:
                    finished = 1

            is_valid, max_end = self.solution.check_solution()

            if not is_valid:
                finished = 1
                if mode :
                    node["start_date"] += 1
                else:
                    node["evac_rate"] -= 1
                self.solution.evac_nodes.update({id_max: node})
            else:
                self.solution.objective = max_end
                old_node = node.copy()
                max_end_old = max_end

        self.solution.evac_nodes.update({id_max : old_node})
        return node, max_end_old, finished

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
    # bound = Bound(Reader("dense_10_30_3_1_I.full").data)
    bound.calculate_upper_bound()
    bound.upper_bound
    neighbour = Neighbour(bound.upper_bound)
    neighbour.local_search_with_a_critical_node()
    neighbour.solution.write_solution("ExempleSimple")



