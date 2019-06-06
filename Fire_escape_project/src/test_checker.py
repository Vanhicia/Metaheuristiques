from solution import *

if __name__ == '__main__':
    display = True
    solution = Solution()

    print("-------------- Test Checker --------------")

    print("\nTest 1: checker verifies the solution corresponding to a lower bound")
    print("Expected result: The solution is not valid")
    print("Result:")
    solution.read_solution("solution_dense_10_30_3_1_I_lower_bound.txt")
    solution.check_solution(display)

    print("\nTest 2: checker verifies the solution corresponding to an upper bound")
    print("Expected result: The solution is valid")
    print("Result:")
    solution.read_solution("solution_dense_10_30_3_1_I_upper_bound.txt")
    solution.check_solution(display)