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


