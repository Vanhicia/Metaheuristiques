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

        # Calculate the upper bound
        bound = Bound(read.data)
        bound.calculate_upper_bound()
        bound.upper_bound.write_solution("solution_" + instance.rstrip(".full"))
        # bound.upper_bound.check_solution()

        # Neighborhood search
        neighbour = Neighbour(bound.upper_bound)
        neighbour.local_search_with_a_critical_node()
        neighbour.solution.write_solution("solution_" + instance.rstrip(".full") + "_neighbourhood")

        # Diversification search
        div = Diversification(read.data)
        div.diversify()
        div.solution.write_solution("solution_" + instance.rstrip(".full") + "_diversification")