from neighbour import *
import sys


class Diversification:

    def __init__(self, data):
        self.data = data
        self.solution = None

    def diversify(self):
        start_prog = time.time()

        # Initialize with the not randomized upper bound
        bound = Bound(self.data)
        obj_min = sys.maxsize
        k = 0  # the counter to stop the diversification
        n = len(bound.data.evac_node_id_list)
        random = True

        # Loop for the diversification :
        # We use the multi-start method
        # Each initial solution is a upper bound calculated with a randomized evacuation order
        # We stop to look for a new neighborhood
        # when the iteration number without solution improvement
        # is superior to the number of equal nodes
        while k < n:
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
                # Reset the counter
                k = 0
                print("\nupdate solution")
                print("min =" + str(obj_min))
            k += 1

        end_prog = time.time()
        timestamp = end_prog - start_prog

        self.solution.method = "Neighbourhood search & Diversification"
        self.solution.timestamp = timestamp


if __name__ == '__main__':
    filename = "ExempleSimple"
    div = Diversification(Reader(filename + ".full").data)
    div.diversify()
    print("diversification solution = " + str(div.solution.objective))