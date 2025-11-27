class TwoDimensionalLine:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
    
    def GetAxisBounds(self, dimension):
        if dimension == 0:
            return (self.start_x, self.end_x)
        elif dimension == 1:
            return (self.start_y, self.end_y)
    
    def SetAxisBounds(self, dimension, min_val, max_val):
        if dimension == 0:
            self.start_x = min_val
            self.end_x = max_val
        elif dimension == 1:
            self.start_y = min_val
            self.end_y = max_val

class ThreeDimensionalLine:
    def __init__(self, start_x, start_y, start_z, end_x, end_y, end_z):
        self.start_x = start_x
        self.start_y = start_y
        self.start_z = start_z
        self.end_x = end_x
        self.end_y = end_y
        self.end_z = end_z
    
    def GetAxisBounds(self, dimension):
        if dimension == 0:
            return (self.start_x, self.end_x)
        elif dimension == 1:
            return (self.start_y, self.end_y)
        elif dimension == 2:
            return (self.start_z, self.end_z)
    
    def SetAxisBounds(self, dimension, min_val, max_val):
        if dimension == 0:
            self.start_x = min_val
            self.end_x = max_val
        elif dimension == 1:
            self.start_y = min_val
            self.end_y = max_val
        elif dimension == 2:
            self.start_z = min_val
            self.end_z = max_val

class Square:
    def __init__(self, min_x, min_y, max_x, max_y):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
    
    def GetBounds(self, dimension):
        if dimension == 0:
            return (self.min_x, self.max_x)
        elif dimension == 1:
            return (self.min_y, self.max_y)
        
class Cube:
    def __init__(self, min_x, min_y, min_z, max_x, max_y, max_z):
        self.min_x = min_x
        self.min_y = min_y
        self.min_z = min_z
        self.max_x = max_x
        self.max_y = max_y
        self.max_z = max_z
    
    def GetBounds(self, dimension):
        if dimension == 0:
            return (self.min_x, self.max_x)
        elif dimension == 1:
            return (self.min_y, self.max_y)
        elif dimension == 2:
            return (self.min_z, self.max_z)

def identify_intersection(line, square) -> bool:
    clipped_line = line
    for i in range(2):
        line_bounds = line.GetAxisBounds(i)
        square_bounds = square.GetBounds(i)

        if line_bounds[0] > square_bounds[1] or line_bounds[1] < square_bounds[0]:
            return False
        else:
            clipped_line.SetAxisBounds(i, max(line_bounds[0], square_bounds[0]), min(line_bounds[1], square_bounds[1]))

    if abs(clipped_line.end_x - clipped_line.start_x) > 0 or abs(clipped_line.end_y - clipped_line.start_y) > 0:
        print(f"Clipped Line Coordinates: Start({clipped_line.start_x}, {clipped_line.start_y}), End({clipped_line.end_x}, {clipped_line.end_y})")
        return True

    return False

def identify_intersection_3d(line, cube) -> bool:
    clipped_line = line
    for i in range(3):
        line_bounds = line.GetAxisBounds(i)
        cube_bounds = cube.GetBounds(i)

        if line_bounds[0] > cube_bounds[1] or line_bounds[1] < cube_bounds[0]:
            return False
        else:
            clipped_line.SetAxisBounds(i, max(line_bounds[0], cube_bounds[0]), min(line_bounds[1], cube_bounds[1]))

    if abs(clipped_line.end_x - clipped_line.start_x) > 0 or abs(clipped_line.end_y - clipped_line.start_y) > 0 or abs(clipped_line.end_z - clipped_line.start_z) > 0:
        print(f"Clipped Line Coordinates: Start({clipped_line.start_x}, {clipped_line.start_y}), End({clipped_line.end_x}, {clipped_line.end_y})")
        return True

    return False

def test1_line_touches_cube_corner():
    print("Test 1: Line touches cube corner")
    test_line = ThreeDimensionalLine(0, 0, 0, 1, 1, 1)
    test_cube = Cube(1, 1, 1, 4, 4, 4)
    return identify_intersection_3d(test_line, test_cube)

def test2_line_inside_cube():
    print("Test 2: Line completely inside cube")
    test_line = ThreeDimensionalLine(2, 2, 2, 3, 3, 3)
    test_cube = Cube(1, 1, 1, 4, 4, 4)
    return identify_intersection_3d(test_line, test_cube)

def test3_line_outside_cube():
    print("Test 3: Line completely outside cube")
    test_line = ThreeDimensionalLine(5, 5, 5, 6, 6, 6)
    test_cube = Cube(1, 1, 1, 4, 4, 4)
    return identify_intersection_3d(test_line, test_cube)

def test4_line_goes_through_cube():
    print("Test 4: Line goes through cube")
    test_line = ThreeDimensionalLine(0, 0, 0, 5, 5, 5)
    test_cube = Cube(1, 1, 1, 4, 4, 4)
    return identify_intersection_3d(test_line, test_cube)


def test1_line_touches_square_corner():
    print("Test 1: Line touches square corner")
    test_line = TwoDimensionalLine(0, 0, 1, 1)
    test_square = Square(1, 1, 4, 4)
    return identify_intersection(test_line, test_square)

def test2_line_inside_square():
    print("Test 2: Line completely inside square")
    test_line = TwoDimensionalLine(2, 2, 3, 3)
    test_square = Square(1, 1, 4, 4)
    return identify_intersection(test_line, test_square)

def test3_line_outside_square():
    print("Test 3: Line completely outside square")
    test_line = TwoDimensionalLine(5, 5, 6, 6)
    test_square = Square(1, 1, 4, 4)
    return identify_intersection(test_line, test_square)

def test4_line_crosses_square():
    print("Test 4: Line crosses square")
    test_line = TwoDimensionalLine(0, 0, 5, 5)
    test_square = Square(1, 1, 4, 4)
    return identify_intersection(test_line, test_square)

def test5_line_bounding_box_overlaps_square_but_no_intersection():
    print("Test 5: Line bounding box overlaps square but no intersection")
    test_line = TwoDimensionalLine(0, 0, 5, 5)
    test_square = Square(0, 3, 1, 4)
    return identify_intersection(test_line, test_square)

def main():
    print("Running 2D Line-Square Intersection Tests:")
    result = test1_line_touches_square_corner()
    print(f"Intersection: {result}")
    result = test2_line_inside_square()
    print(f"Intersection: {result}")
    result = test3_line_outside_square()
    print(f"Intersection: {result}")
    result = test4_line_crosses_square()
    print(f"Intersection: {result}")
    result = test5_line_bounding_box_overlaps_square_but_no_intersection()
    print(f"Intersection: {result}")


    print("\nRunning 3D Line-Cube Intersection Tests:")
    result = test1_line_touches_cube_corner()
    print(f"Intersection: {result}")
    result = test2_line_inside_cube()
    print(f"Intersection: {result}")
    result = test3_line_outside_cube()
    print(f"Intersection: {result}")
    result = test4_line_goes_through_cube()
    print(f"Intersection: {result}")

if __name__ == "__main__":
    main()
