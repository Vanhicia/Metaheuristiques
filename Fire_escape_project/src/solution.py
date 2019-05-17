

class Solution:

    def __init__(self, filename, bound):
        self.filename = filename
        self.bound = bound

    def write_solution(self, mode):
        file = open(self.filename+".txt", "w+")
        file.write(self.filename)  # Nom de l'instance résolue
        file.write(str(len(self.bound.tree.evac_node_id_list)))  # <nombre de sommets à évacuer>
        if mode == 0:  # Lower bound
            for evac_node in self.bound.tree.evac_node_id_list:
                # pour chaque sommet à évacuer :
                # <son identifiant>, <son taux d’évacuation>, <sa date de début d’évacuation>
                file.write(evac_node.id1 + " " + evac_node.max_rate + " 0")
                file.write("invalid")  # nature de la solution : <valid ou invalid>
                file.write("inf")  # <valeur de la fonction objectif>
                file.write(self.bound.timestamp_lower_bound)    # <temps de calcul>
                # <méthode> : le nom de la méthode utilisée et la version de l’implémentation
                file.write("handmade 0.1.0")
                # champ libre (paramètre de la méthode, nom du binôme, ....)
                file.write("everyone evacuates from start ; no constraint check")
        else:
            pass





