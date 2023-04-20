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

import numpy as np
import sys
import itertools

class GridTraversal():
    
    def __init__(self): 
        self.__infinity__ = sys.maxsize

        with open("test_input.txt") as f:
            self.__maze__ = [list(line.strip()) for line in f]

        self.__avocado_positions__ = []

        # Find the start position and avocado positions
        for row in range(len(self.__maze__)):
            for col in range(len(self.__maze__[row])):
                if self.__maze__[row][col] == "x":
                    self.__robot_row__, self.__robot_col__ = row, col
                elif self.__maze__[row][col] == "@":
                    self.__avocado_positions__.append((row, col))

        self.buildDistanceMatrix()

        # print(np.matrix(self.__avocado_positions__).transpose())
        print("---------------------------")
        print(np.matrix(self.__distanceMat__))

    
    def bfs(self, start_row, start_col):
        """
        Breadth-first search algorithm, which is guaranteed to find the shortest
        path between arbitrary start and destination points in an unweighted graph
        """
 
        bfs_depth_tracker = [
            [-1 for i in range(len(self.__maze__[0]))] for j in range(
                                                        len(self.__maze__))]
        queue = [(start_row, start_col, 0)]
        visited = set((start_row, start_col))

        while queue:
            row, col, steps = queue.pop(0)
            if(bfs_depth_tracker[row][col] == -1):
                bfs_depth_tracker[row][col] = steps

            for drow, dcol in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row < len(self.__maze__) and \
                0 <= new_col < len(self.__maze__[0]) and \
                (new_row, new_col) not in visited and self.__maze__[new_row][new_col] != "#":
                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))
        
        return bfs_depth_tracker


    def buildDistanceMatrix(self):
        """ 
        Distance matrix = [n + 1][n +1] where n = number of avocados
        0th index on row and column axis represents start position of robot
        ith index where i>0 represents the avocado at index i of avocado_positions array

        Value at distance_mat[i][j] = distance[j][i] = shortest path length between ith 
        and jth avocado (where start position counts as avocado as well) 
        """

        self.__distanceMat__ = [
            [0 for i in range(len(self.__avocado_positions__) + 1)]  \
                for j in range(len(self.__avocado_positions__) + 1)]


        for i in range(len(self.__distanceMat__)):
            if (i == 0): start_row, start_col = self.__robot_row__, self.__robot_col__
            else: start_row, start_col = self.__avocado_positions__[i-1]

            bfs_depth_tracker = self.bfs(start_row, start_col)

            for avo_idx in range(len(self.__avocado_positions__)):
                if(i == avo_idx + 1): continue
                avocado_pos = self.__avocado_positions__[avo_idx]
                self.__distanceMat__[avo_idx+1][i] = bfs_depth_tracker[avocado_pos[0]][avocado_pos[1]]
                self.__distanceMat__[i][avo_idx+1] = bfs_depth_tracker[avocado_pos[0]][avocado_pos[1]]
                
        return
    
    def determineBestPath(self):
        """
        Implementation of Held-Karp, an algorithm that solves the Traveling
        Salesman Problem using dynamic programming with memoization.

        Returns: A tuple, (cost, path).
        """

        n = len(self.__distanceMat__)

        # Maps each subset of the nodes to the cost to reach that subset, as well
        # as what node it passed before reaching this subset.
        # Node subsets are represented as set bits.
        C = {}

        # Set transition cost from initial state
        for k in range(1, n):
            C[(1 << k, k)] = (self.__distanceMat__[0][k], 0)

        # Iterate subsets of increasing length and store intermediate results
        # in classic dynamic programming manner
        for subset_size in range(2, n):
            for subset in itertools.combinations(range(1, n), subset_size):
                # Set bits for all nodes in this subset
                bits = 0
                for bit in subset:
                    bits |= 1 << bit

                # Find the lowest cost to get to this subset
                for k in subset:
                    prev = bits & ~(1 << k)

                    res = []
                    for m in subset:
                        if m == 0 or m == k:
                            continue
                        res.append((C[(prev, m)][0] + self.__distanceMat__[m][k], m))
                    C[(bits, k)] = min(res)

        # We're interested in all bits but the least significant (the start state)
        bits = (2**n - 1) - 1

        # Calculate optimal cost
        res = []
        for k in range(1, n):
            res.append((C[(bits, k)][0] + self.__distanceMat__[k][0], k))
            
        opt, parent = min(res)

        # Backtrack to find full path
        path = []
        for i in range(n - 1):
            path.append(parent)
            new_bits = bits & ~(1 << parent)
            _, parent = C[(bits, parent)]
            bits = new_bits

        # Add implicit start state

        return opt - self.__distanceMat__[path[-1]][0], list(path)



def main():
    print("Hello world!")
    gt = GridTraversal()

    path_len, path = gt.determineBestPath()
    print(np.matrix(path))
    print("---------------------")
    print(np.matrix([gt.__avocado_positions__[i-1] for i in path]).transpose())
    print("---------------------")
    print("Path length: ", path_len)

if __name__ == "__main__":
    main()