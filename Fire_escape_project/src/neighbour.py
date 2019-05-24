from pathlib import Path
import math

class Neighbour:

    def __init__(self):
        self.instance = None
        self.evac_nodes = {}
        self.valid = None
        self.objective = None
        self.list_neighbours = None
        self.data = None

    def set_initial_solution_from_file(self, path):
        data_folder = Path("../solutions/")
        file_to_open = data_folder / path

        with open(file_to_open, "r") as f:
            self.instance = f.readline().rstrip('\n\r') + ".txt"

            evac_node_nb = int(f.readline())

            # Evac node information
            for k in range(evac_node_nb):
                id1, evac_rate, start_date = map(int, f.readline().rstrip('\n\r').split(" "))
                self.evac_nodes[id1] = {"evac_rate": evac_rate, "start_date": start_date}

            valid = f.readline().rstrip('\n\r')
            if valid == "valid":
                self.valid = True
            elif valid == "invalid":
                self.valid = False
            else:
                raise SyntaxError

            self.objective = int(f.readline())



    def local_search(self):
        # Find the most constraint node
        # Change Start_date until not valid and stop at the state that is valid
        # Change Max_rate
        #
        pass
        # self.evac_nodes[id1]
        # modif max_rate and start date
        # test different objective functions

    # Return the evac node id for which the evacuation is the last to terminate
    # according the evacuation info given in parameter
    def find_critical_evac(self, evac_nodes):
        max_evac = None
        max_end = 0
        for evac_node_id, evac_rate, strat_date in evac_nodes.items():
            end = self.calculate_end_evac(evac_node_id, evac_rate, strat_date)

            if max_end < end:
                max_end = end
                max_evac = evac_node_id

        return max_evac

    # Calculate the end time of the evacuation for the given evac node
    # warning : this function does not verify if an arc capacity is exceeded
    def calculate_end_evac(self, evac_node_id, evac_rate, start_date):
        evac_node = self.data.nodes[evac_node_id]
        father_arc = evac_node.father
        father_arc_aux = father_arc

        # look for the last arc of the evacuation road
        while father_arc.father.id1 != self.data.safe_node_id:
            father_arc = father_arc_aux

        interval = father_arc.evac[evac_node_id] # interval between the evac node and the safe node
        end = start_date + interval + math.ceil(evac_node.population / evac_rate)

        return end




