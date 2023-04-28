import sys
import itertools

class DPGridTraversal():    
    def __init__(self, input_filename): 
        self.__infinity__ = sys.maxsize
        self.__input__ = input_filename

        with open(self.__input__) as f:
            self.__maze__ = [list(line.strip()) for line in f]

        self.__avocado_positions__ = []

        # Find the start position and avocado positions
        for row in range(len(self.__maze__)):
            for col in range(len(self.__maze__[row])):
                if self.__maze__[row][col] == "x":
                    self.__robot_row__, self.__robot_col__ = row, col
                elif self.__maze__[row][col] == "@":
                    self.__avocado_positions__.append((row, col))

        self.build_distance_matrix()
    
    def bfs(self, start_row, start_col):
        """
        Breadth-first search algorithm, which is guaranteed to find the shortest
        path between arbitrary start and destination points in an unweighted graph
        """
        
        bfs_depth_tracker = [[-1 for _ in range(len(self.__maze__[0]))] \
                             for _ in range(len(self.__maze__))]
        
        queue = [(start_row, start_col, 0)]
        visited = set((start_row, start_col))

        while queue:
            row, col, steps = queue.pop(0)
            
            if(bfs_depth_tracker[row][col] == -1):
                bfs_depth_tracker[row][col] = steps

            for drow, dcol in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                
                new_row, new_col = row + drow, col + dcol

                if  0 <= new_row < len(self.__maze__) and \
                    0 <= new_col < len(self.__maze__[0]) and \
                    (new_row, new_col) not in visited and \
                    self.__maze__[new_row][new_col] != "#":

                    queue.append((new_row, new_col, steps + 1))
                    visited.add((new_row, new_col))
        
        return bfs_depth_tracker

    def build_distance_matrix(self):
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
    
    def determine_best_path(self):
        """
        Returns: A tuple, (cost, path).
        """

        path_size = len(self.__distanceMat__) # of avocados + 1

        """
        Hashmap to map each subset of the nodes to a corresponding cost to reach that subset from the start node;
        Also tracks which node it passed before reaching this subset. Node subsets are represented as set bits.
        Key of costmap is a pair: (binary representation of set of nodes in subset, index of node)
        Value of costmap is a pair: (distance from start, node passed to get there)
        """
        cost_map = {} 

        for k in range(1, path_size):
            cost_map[(1 << k, k)] = (self.__distanceMat__[0][k], 0)  # Set transition cost from initial state

        # Iterate subsets of increasing length and store intermediate results
        for subset_size in range(2, path_size):
            for subset in itertools.combinations(range(1, path_size), subset_size):
                
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
                        
                        res.append((cost_map[(prev, m)][0] + self.__distanceMat__[m][k], m))

                    cost_map[(bits, k)] = min(res) # Store lowest cost to arrive at subset in cost map

        bits = (2**path_size - 1) - 1 # Bit mask with all 1s for all avocados; 0 for start state

        # Calculate optimal cost
        res = []
        for k in range(1, path_size):
            res.append((cost_map[(bits, k)][0], k)) # + self.__distanceMat__[k][0],
            
        opt, parent = min(res)

        # Backtrack to find full path
        path = []
        for _ in range(path_size - 1):
            path.append(parent)
            new_bits = bits & ~(1 << parent)
            _, parent = cost_map[(bits, parent)]
            bits = new_bits

        return opt, list(path)

