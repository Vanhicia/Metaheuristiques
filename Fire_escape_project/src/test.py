import os
from reader import *
from bound import *


if __name__ == '__main__':
    instance_list = os.listdir("../instances")
    instance_list.remove("TD.txt")

    for instance in instance_list[2:]:
        read = Reader(instance)

        # Calculate the upper bound
        bound = Bound(read.data)
        bound.calculate_upper_bound()
        bound.upper_bound.write_solution("solution_" + instance.rstrip(".full"))
