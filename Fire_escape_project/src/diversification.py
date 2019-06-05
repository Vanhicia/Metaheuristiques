from neighbour import *
import sys


class Diversification:

    def __init__(self, data):
        self.data = data
        self.solution = None

    # parameter : the number of starts
    def diversify(self, iteration_nb):
        start_prog = time.time()

        # Initialize with the not randomized upper bound
        bound = Bound(self.data)
        obj_min = sys.maxsize
        k = 0  # the counter to stop the diversification
        random = True

        # Loop for the diversification :
        # We use the multi-start method
        # Each initial solution is an upper bound calculated with a randomized evacuation order
        while k < iteration_nb:
            # Calculate a new initial solution
            bound.calculate_upper_bound(random)
            # Search the local optimal solution in the neighbourhood of this solution
            neighbour = Neighbour(bound.upper_bound)
            neighbour.local_search_with_a_critical_node()
            # If the local solution is better than the previous solution
            if obj_min > neighbour.solution.objective:
                # Update the solution
                self.solution = neighbour.solution
                obj_min = self.solution.objective
                # print("\nupdate solution")
                # print("min =" + str(obj_min))
            k += 1

        end_prog = time.time()
        timestamp = end_prog - start_prog

        self.solution.method = "Neighbourhood search & Diversification (n=" + str(iteration_nb) + ")"
        self.solution.timestamp = timestamp


if __name__ == '__main__':
    filename = "ExempleSimple"
    div = Diversification(Reader(filename + ".full").data)
    div.diversify(10)
    print("diversification solution = " + str(div.solution.objective))
