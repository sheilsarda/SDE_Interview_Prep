import itertools
input_file_name = "tests/test_input_1.txt"

# Read the input file
with open(input_file_name) as f:
    maze = [list(line.strip()) for line in f]

# Initialize variables
start_row, start_col = None, None
avocado_positions = []

# Find the start position and avocado positions
for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == "x":
            start_row, start_col = row, col
        elif maze[row][col] == "@":
            avocado_positions.append((row, col))

robot_row, robot_col = start_row, start_col

# Define a function to find the shortest path between two points using BFS
def bfs(maze, start_row, start_col, dest_row, dest_col):
    queue = [(start_row, start_col, 0)]
    visited = set((start_row, start_col))
    while queue:
        row, col, steps = queue.pop(0)
        if row == dest_row and col == dest_col:
            return steps
        for drow, dcol in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and \
               (new_row, new_col) not in visited and maze[new_row][new_col] != "#":
                queue.append((new_row, new_col, steps + 1))
                visited.add((new_row, new_col))
    return None


# Not all of them are valid; need BFS to tell us where obstacles block traversal
all_permutations = list(itertools.permutations(avocado_positions))
permutation_path_lengths = []

for path_permutation in all_permutations:
    # Step 1: determine feasibility
    # Step 2: determine number of steps

    total_path_length = 0
    start_row, start_col = robot_row, robot_col

    for avocado_position in path_permutation:
        dest_row, dest_col = avocado_position[0], avocado_position[1]
        
        steps_for_segment = bfs(maze, start_row, start_col, dest_row, dest_col)
        
        if(steps_for_segment == None):
            break
        
        total_path_length += steps_for_segment
        start_row, start_col = avocado_position[0], avocado_position[1]
    
    if(steps_for_segment == None):
        permutation_path_lengths.append(None)
    else:    
        permutation_path_lengths.append(total_path_length)

print("Min path length found: ", min(permutation_path_lengths))
print("Min Path permuation: ", 
        all_permutations[permutation_path_lengths.index(min(permutation_path_lengths))])
