

class Solution:

    def __init__(self, filename, data, solution_node_list, is_valid, objective, timestamp, method, other):
        self.filename = filename
        self.data = data
        self.solution_node_list = solution_node_list
        self.is_valid = is_valid
        self.objective = objective
        self.timestamp = timestamp
        self.method = method
        self.other = other

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






