import numpy as np
from dynamic_prog_sol import DPGridTraversal
from brute_force_sol import BruteForceGridTraversal

tests_to_run = [1]

input_file_str = "tests/test_input_"
output_file_str = "tests/test_output_"

approach = "brute_force" # "brute_force" or "dynamic_prog"

def main():

    for test_idx in tests_to_run:
        input_filename = input_file_str + str(test_idx) + ".txt"
        output_filename = output_file_str + str(test_idx) + ".txt"

        if approach == "dynamic_prog":
            # Dynamic Programming Soln
            dp_soln = DPGridTraversal(input_filename, output_filename)
            path_len, path = dp_soln.determine_best_path()

            print("Path length: ", path_len)
            print(np.matrix([dp_soln.__avocado_positions__[i-1] for i in path]).transpose())

        else:
            # Brute Force Soln
            bf_soln = BruteForceGridTraversal(input_filename, output_filename)
            bf_soln.determine_best_path()

if __name__ == "__main__":
    main()
