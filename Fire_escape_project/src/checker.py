from pathlib import Path
from data_structure import *
from reader import *


class Checker:

    def __init__(self, path):

        # Open the file
        data_folder = Path("../solutions/")
        file_to_open = data_folder / path

        with open(file_to_open, "r") as f:

            self.instance = f.readline().rstrip('\n\r')
            evac_node_nb = int(f.readline())
            self.evac_nodes = []

            # Evac node information
            for k in range(evac_node_nb):
                id, evac_rate, start_date = f.readline.split(" ")
                self.evac_nodes.append({"id": id, "evac_rate": evac_rate, "start_date": start_date})

            valid = f.readline().rstrip('\n\r')
            if valid == "valid":
                self.valid = True
            elif valid == "invalid":
                self.valid = False
            else:
                raise SyntaxError

            self.objective = int(f.readline())

    def check_solution(self):
        reader = Reader(self.instance)

        #TODO