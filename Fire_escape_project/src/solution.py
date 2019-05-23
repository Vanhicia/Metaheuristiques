from reader import *


class Solution:

    def __init__(self, filename=None, data=None, evac_nodes=None, is_valid=None, objective=None, timestamp=None, method=None, other=None):
        self.filename = filename
        self.data = data
        self.evac_nodes = evac_nodes  # dictionary for the evac nodes (key = id, info = evac_rate & start_date)
        self.is_valid = is_valid
        self.objective = objective
        self.timestamp = timestamp
        self.method = method
        self.other = other

    def check_solution(self):
        time_limit = 1000
        if self.data is None :
            self.data = Reader(self.filename).data
        arc_nb = len(self.data.arcs)
        max_end = 0

        gantt = np.zeros((arc_nb, time_limit))

        k = 0
        for arc in self.data.arcs.values():

            for id1, interval in arc.evac.items():
                is_max = False
                evac_node = self.data.nodes[id1]
                evac_info = self.evac_nodes[id1]

                beg = evac_info['start_date'] + interval
                end = int(beg + (evac_node.population//evac_info['evac_rate']))

                if max_end < (end + arc.time):
                    is_max = True
                    max_end = end + arc.time

                for i in range(beg, end):
                    gantt[k][i] += evac_info['evac_rate']

                rest = evac_node.population % evac_info['evac_rate']
                if rest != 0:
                    gantt[k][end] += rest
                    if is_max:
                        max_end += 1

            # Check the capacity is not exceeded
            for i in range(time_limit):
                # If the solution is not valid
                if arc.capacity < gantt[k][i]:
                    if not self.is_valid:
                        return True
                    else:
                        return False

            k += 1

        print("The solution is valid")
        if self.objective == max_end:
            print("Objective : " + str(max_end))
        else:
            print("The objective is wrong : it is %d, instead of %d", max_end, self.objective)

        return True

    def read_solution(self, solution_file):

        # Open the file
        data_folder = Path("../solutions/")
        file_to_open = data_folder / solution_file

        with open(file_to_open, "r") as f:

            self.filename = f.readline().rstrip('\n\r') + ".txt"
            evac_node_nb = int(f.readline())
            self.evac_nodes = {}

            # Evac node information
            for k in range(evac_node_nb):
                id1, evac_rate, start_date = map(int, f.readline().rstrip('\n\r').split(" "))
                self.evac_nodes[id1] = {"evac_rate": evac_rate, "start_date": start_date}

            valid = f.readline().rstrip('\n\r')
            if valid == "valid":
                self.is_valid = True
            elif valid == "invalid":
                self.is_valid = False
            else:
                raise SyntaxError

            self.objective = int(f.readline())

    def write_solution(self):
        file = open("solution_" + self.filename+".txt", "w+")
        file.write(self.filename)  # Nom de l'instance résolue
        file.write(str(len(self.data.evac_node_id_list)))  # <nombre de sommets à évacuer>
        for evac_node in self.data.evac_node_id_list:
            # pour chaque sommet à évacuer :
            # <son identifiant>, <son taux d’évacuation>, <sa date de début d’évacuation>
            file.write(evac_node.id1 + " " + evac_node.max_rate + " 0")

            # nature de la solution : <valid ou invalid>
            if self.is_valid:
                file.write("valid")
            else:
                file.write("invalid")

            file.write(self.objective)  # <valeur de la fonction objectif>

            file.write(self.timestamp )   # <temps de calcul>

            # <méthode> : le nom de la méthode utilisée et la version de l’implémentation
            file.write(self.method)

            # champ libre (paramètre de la méthode, nom du binôme, ....)
            file.write(self.other)


if __name__ == '__main__':
    solution = Solution()
    solution.read_solution("solution_TD_non_opti.txt")
    print(solution.check_solution())
    #solution.write_solution()





