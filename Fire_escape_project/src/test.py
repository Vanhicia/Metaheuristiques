import os
from reader import *
from bound import *
from neighbour import *
from diversification import *


if __name__ == '__main__':
    instance_list = os.listdir("../instances")
    instance_list.remove("TD.txt")

    for instance in instance_list:
        read = Reader(instance)
        print(instance)

        # Calculate the lower and upper bound
        bound = Bound(read.data)
        bound.calculate_lower_bound()
        bound.lower_bound.write_solution("solution_" + instance.rstrip(".full") + "_lower_bound")
        bound.calculate_upper_bound()
        bound.upper_bound.write_solution("solution_" + instance.rstrip(".full") + "_upper_bound")

        # Neighborhood search
        neighbour = Neighbour(bound.upper_bound)
        neighbour.local_search_with_a_critical_node()
        neighbour.solution.write_solution("solution_" + instance.rstrip(".full") + "_neighbourhood")

        # Diversification search
        div = Diversification(read.data)
        div.diversify(5)
        div.solution.write_solution("solution_" + instance.rstrip(".full") + "_diversification_n=5")
        div.diversify(10)
        div.solution.write_solution("solution_" + instance.rstrip(".full") + "_diversification_n=10")
        div.diversify(20)
        div.solution.write_solution("solution_" + instance.rstrip(".full") + "_diversification_n=20")