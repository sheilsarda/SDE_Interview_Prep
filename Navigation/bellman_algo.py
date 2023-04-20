"""
Input: text file representing the 2D map, where: 
• “#”   = obstacles 
• “.”    = open path 
• “@” = avocado 
• “x”   = starting location

################
###..#@.....@#.#
##x....####..#.#
###.....#...##.#
#######.#.###..#
#@#...#..@....##
#...#...#.###.@#
################

Output: text file, where: 
• The first line is the minimum number of grid moves the robot must make 
• Each following line is a coordinate: [row, col], sorted from first avocado location to the last 

Assumptions: 
• The robot can only move in four directions: up, down, left, and right 
• The robot does not need to return to the initial starting location 
• The robot moves at constant speed, so each grid move requires the same amount of time 
• The robot can revisit the same grid point, and the avocado can be picked up during any of the visits 

Pseudocode
1) Find distance from starting location to all avocados
"""



class GridTraversal():
    
    def __init__(self): 
        self.__infinity__ = 100000000

        with open("test_input.txt") as f:
            self.__maze__ = [list(line.strip()) for line in f]

        self.__start_row__, self.__start_col__ = None, None
        self.__avocado_positions__ = []
        self.__bfs_depth_tracker__ = [
            [-1 for i in range(len(self.__maze__[0]))] for j in range(
                                                        len(self.__maze__))]

        # Find the start position and avocado positions
        for row in range(len(self.__maze__)):
            for col in range(len(self.__maze__[row])):
                if self.__maze__[row][col] == "x":
                    self.__start_row__, self.__start_col__ = row, col
                elif self.__maze__[row][col] == "@":
                    self.__avocado_positions__.append((row, col))

        self.__robot_row__, self.__robot_col__ = self.__start_row__, self.__start_col__

        # Find distance to every avocado from start position and find the nearest one
        self.bfs(self.__robot_row__, self.__robot_col__)

        self.__distanceMatrix__ = self.buildDistanceMatrix()

    
    def bfs(self, start_row, start_col):

        queue = [(start_row, start_col, 0)]
        visited = set((start_row, start_col))

        while queue:
            row, col, steps = queue.pop(0)
            if(self.__bfs_depth_tracker__[row][col] == -1):
                self.__bfs_depth_tracker__[row][col] = steps

            for drow, dcol in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row < len(self.__maze__) and \
                0 <= new_col < len(self.__maze__[0]) and \
                (new_row, new_col) not in visited and self.__maze__[new_row][new_col] != "#":
                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))

    def buildDistanceMatrix(self):
        return
    
    def determineBestPath(self):
        return
    
def main():
    print("Hello world!")

if __name__ == "__main__":
    main()