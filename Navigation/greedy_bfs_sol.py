import itertools

"""
Notes after evaluating the sample test case is that the order of avocados to collect is correct, but the 
total number of steps to get all of them is overstated. 

Suspected root cause: it defaults to picking avocados by traversing the matrix from left to right and top 
to bottom, and then sorts them into the final output list based on the number of steps it takes to go from
start pos to 1st avo (from matrix order), and then from that avo to the next, etc.

As a potential solution, first determine bfs depth for all avocados, and make the 1st avo the closest bfs
distance. One downside is that this greedy optimization might not be long term optimal
"""

# Read the input file
with open("test_input.txt") as f:
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


# Not all of them are valid; need BFS to tell us where obstacles block traversal
all_permutations = list(itertools.permutations(avocado_positions))
# all_permutations = all_permutations[:2]
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
            steps_for_segment = -1
            break
        
        total_path_length += steps_for_segment
        start_row, start_col = avocado_position[0], avocado_position[1]
    
    permutation_path_lengths.append(total_path_length)

for i in range(0, len(all_permutations)):
    print("Permutation: ", all_permutations[i])
    print("Path length: ", permutation_path_lengths[i])

print("------------------------------------")
print("Min path length found: ", min(permutation_path_lengths))
print("Min Path permuation: ", 
        all_permutations[permutation_path_lengths.index(min(permutation_path_lengths))])