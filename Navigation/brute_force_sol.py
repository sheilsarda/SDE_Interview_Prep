import itertools
input_file_name = "tests/test_input_1.txt"

class BruteForceGridTraversal():
    def __init__(self, input_filename, output_filename):    
        
        # Read the input file
        with open(input_filename) as f:
            self.__maze__ = [list(line.strip()) for line in f]

        # Initialize variables
        start_row, start_col = None, None
        self.__avocado_positions__ = []
        self.__output_filename__ = output_filename
        
        # Find the start position and avocado positions
        for row in range(len(self.__maze__)):
            for col in range(len(self.__maze__[row])):
                if self.__maze__[row][col] == "x":
                    start_row, start_col = row, col
                elif self.__maze__[row][col] == "@":
                    self.__avocado_positions__.append((row, col))

        self.__robot_row__, self.__robot_col__ = start_row, start_col

    def bfs(self, start_row, start_col, dest_row, dest_col):
        queue = [(start_row, start_col, 0)]
        visited = set((start_row, start_col))
        while queue:
            row, col, steps = queue.pop(0)
            if row == dest_row and col == dest_col:
                return steps
            for drow, dcol in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row < len(self.__maze__) and 0 <= new_col < len(self.__maze__[0]) and \
                (new_row, new_col) not in visited and self.__maze__[new_row][new_col] != "#":
                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))
        return None

    def determine_best_path(self):
        # Not all of them are valid; need BFS to tell us where obstacles block traversal
        all_permutations = list(itertools.permutations(self.__avocado_positions__))
        permutation_path_lengths = []

        for path_permutation in all_permutations:
            # Step 1: determine feasibility
            # Step 2: determine number of steps

            total_path_length = 0
            start_row, start_col = self.__robot_row__, self.__robot_col__

            for avocado_position in path_permutation:
                dest_row, dest_col = avocado_position[0], avocado_position[1]
                
                steps_for_segment = self.bfs(start_row, start_col, dest_row, dest_col)
                
                if(steps_for_segment == None):
                    break
                
                total_path_length += steps_for_segment
                start_row, start_col = avocado_position[0], avocado_position[1]
            
            if(steps_for_segment == None):
                permutation_path_lengths.append(None)
            else:    
                permutation_path_lengths.append(total_path_length)

        min_path = all_permutations[permutation_path_lengths.index(min(permutation_path_lengths))]
        min_pathlen = min(permutation_path_lengths) 

        # Open a text file for writing
        with open(self.__output_filename__, 'w') as file:
            file.write(str(min_pathlen) + '\n') # Write min path length            
            
            # Loop through each avocado in path
            for avocado_pos in min_path:
                file.write(str(avocado_pos[0]) + ',' + str(avocado_pos[1]) + '\n')

        print("Min path length found: ", min(permutation_path_lengths))
        print("Min Path permuation: ", 
                all_permutations[permutation_path_lengths.index(min(permutation_path_lengths))])
