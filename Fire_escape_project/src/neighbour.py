from pathlib import Path


class Neighbour:

    def __init__(self):
        self.instance = None
        self.evac_nodes = {}
        self.valid = None
        self.objective = None
        self.list_neighbours = None

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

