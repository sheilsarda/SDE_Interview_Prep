import numpy as np

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
bfs_depth_tracker = [[-1 for i in range(len(maze[0]))] for j in range(len(maze))]


# Find the start position and avocado positions
for row in range(len(maze)):
    for col in range(len(maze[row])):
        if maze[row][col] == "x":
            start_row, start_col = row, col
        elif maze[row][col] == "@":
            avocado_positions.append((row, col))

robot_row, robot_col = start_row, start_col

# Define a function to find the shortest path between two points using BFS
def bfs(maze, start_row, start_col):
    
    queue = [(start_row, start_col, 0)]
    visited = set((start_row, start_col))

    while queue:
        row, col, steps = queue.pop(0)
        if(bfs_depth_tracker[row][col] == -1):
            bfs_depth_tracker[row][col] = steps

        for drow, dcol in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            new_row, new_col = row + drow, col + dcol
            if 0 <= new_row < len(maze) and 0 <= new_col < len(maze[0]) and \
               (new_row, new_col) not in visited and maze[new_row][new_col] != "#":
                queue.append((new_row, new_col, steps + 1))
                visited.add((new_row, new_col))

print(robot_row, robot_col)

# Find distance to every avocado from start position and find the nearest one
bfs(maze, robot_row, robot_col)

distance_to_avocados = []
for avocado in avocado_positions:
    distance_to_avocados.append(bfs_depth_tracker[avocado[0]][avocado[1]])

print(np.matrix(bfs_depth_tracker))

print("Avocados with distances: ")
for i in range(len(avocado_positions)):
    print(avocado_positions[i], " : ", distance_to_avocados[i])

start_pos = avocado_positions[distance_to_avocados.index(min(distance_to_avocados))]
start_index = distance_to_avocados.index(min(distance_to_avocados))
optimal_avocado_path = [start_pos]

last_avocado_pos = start_pos
last_avocado_index = start_index

# for i in range(len(avocado_positions) - 1):
for i in range(1):
    avocado_positions.pop(last_avocado_index)
    distance_to_avocados = []

    current_depth = bfs_depth_tracker[last_avocado_pos[0]][last_avocado_pos[1]]
    
    for avocado_pos in avocado_positions:
        # Calc new distances from this first avocado
        distance_to_avocados.append(bfs_depth_tracker[avocado_pos[0]][avocado_pos[1]] - current_depth)

    print(distance_to_avocados)

print(optimal_avocado_path)