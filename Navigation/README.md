# Avocado path-finding 

## Problem specs 

### Input

A text file representing the 2D map, where: 

| Symbol | Representation |
|--|--|
| `#` | Obstacles | 
| `.` | Open path | 
| `@` | Avocado   |
| `x` | Starting location |

### Output

A text file, where: 

- The first line is the minimum number of grid moves the robot must make 
- Each following line is a coordinate: [row, col], sorted from first avocado location to the last 

### Assumptions
 
- The robot can only move in four directions: up, down, left, and right 
- The robot does not need to return to the initial starting location 
- The robot moves at constant speed, so each grid move requires the same amount of time 
- The robot can revisit the same grid point, and the avocado can be picked up during any of the visits 

## Implementation Details

### Approach 1: Brute Force

**Pseudocode / Algorithm description**

1. Determine location of avocados and start location by traversing grid in row-major order
1. Generate all permutations of start location followed by all avocados
1. Use BFS to determine total path lengths for each permutation generated
1. Choose minimum path length and print out the corresponding path

**Time complexity**

`n` is number of avocados; upper bounded as `r*c`
`r` is number of rows
`c` is number of cols

1. Time complexity of a single BFS run: `O(V+E)`
    1. Number of vertices and edges both bounded at `r*c`
    1. Upper bound on BFS run: `O(r*c)`
1. Time complexity of evaluating each permutation:
    1. `n!` permutations of paths available since start position is always fixed
    1. Each permutation requires `n` iterations of BFS to total distance
    1. Time complexity of total number of permutations: `O(r*c*n*n!) = O(r*c*(n+1)!)`
    1. Given `n <= r*c`, `O(r*c *(n+1)!) = O((r*c) * (r*c + 1)!) = O((r*c + 2)!)`

**Total time complexity of brute force approach is `O((r*c + 2)!)`**

### Approach 2: Dynamic Programming / Memoization 

**Pseudocode / Algorithm description**

1. Determine location of avocados and start location by traversing grid in row-major order
1. Generate all permutations of start location followed by all avocados
1. Use BFS to determine total path lengths for each permutation generated
1. Choose minimum path length and print out the corresponding path

**Time complexity**

`n` is number of avocados; upper bounded as `r*c`
`r` is number of rows
`c` is number of cols

1. Time complexity of a single BFS run: `O(V+E)`
    1. Number of vertices and edges both bounded at `r*c`
    1. Upper bound on BFS run: `O(r*c)`
1. Time complexity of evaluating each permutation:
    1. `n!` permutations of paths available since start position is always fixed
    1. Each permutation requires `n` iterations of BFS to total distance
    1. Time complexity of total number of permutations: `O(r*c*n*n!) = O(r*c*(n+1)!)`
    1. Given `n <= r*c`, `O(r*c *(n+1)!) = O((r*c) * (r*c + 1)!) = O((r*c + 2)!)`

**Total time complexity of brute force approach is `O((r*c + 2)!)`**



![](Time_Complexity_Benchmarking.png)

