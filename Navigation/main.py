import numpy as np
from dynamic_prog_sol import DPGridTraversal
from brute_force_sol import BruteForceGridTraversal

input_file = "tests/test_input_1.txt"

def main():

    # Dynamic Programming Soln
    dp_soln = DPGridTraversal(input_file)
    path_len, path = dp_soln.determine_best_path()

    print("Path length: ", path_len)
    print(np.matrix([dp_soln.__avocado_positions__[i-1] for i in path]).transpose())

    print("---------------------")

    # Brute Force Soln
    bf_soln = BruteForceGridTraversal(input_file)
    bf_soln.determine_best_path()

if __name__ == "__main__":
    main()
