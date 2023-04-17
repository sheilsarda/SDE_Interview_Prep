# Input: text file representing the 2D map, where: 
# • “#”   = obstacles 
# • “.”    = open path 
# • “@” = avocado 
# • “x”   = starting location  
 
# Output: text file, where: 
# • The first line is the minimum number of grid moves the robot must make 
# • Each following line is a coordinate: [row, col], sorted from first avocado location to the last 

# Assumptions: 
# • The robot can only move in four directions: up, down, left, and right 
# • The robot does not need to return to the initial starting location 
# • The robot moves at constant speed, so each grid move requires the same amount of time 
# • The robot can revisit the same grid point, and the avocado can be picked up during any of the visits 

def main():
    return