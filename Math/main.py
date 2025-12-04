import copy
import unittest
from typing import Tuple

class Line:
    def __init__(self, *args: int | float):
        if len(args) % 2 != 0:
            raise ValueError("Line requires an even number of coordinates (start and end points).")
        self.dims = len(args) // 2
        self.start = list(args[:self.dims])
        self.end = list(args[self.dims:])
    
    def get_axis_bounds(self, dimension: int) -> Tuple[float, float]:
        return (self.start[dimension], self.end[dimension])
    
    def set_axis_bounds(self, dimension: int, min_val: float, max_val: float) -> None:
        self.start[dimension] = min_val
        self.end[dimension] = max_val

class Box:
    def __init__(self, *args: int | float):
        if len(args) % 2 != 0:
            raise ValueError("Box requires an even number of coordinates (min and max points).")
        self.dims = len(args) // 2
        self.min_coords = list(args[:self.dims])
        self.max_coords = list(args[self.dims:])
    
    def get_bounds(self, dimension: int) -> Tuple[float, float]:
        return (self.min_coords[dimension], self.max_coords[dimension])

def identify_intersection(line: Line, box: Box) -> bool:
    
    if line.end < box.min_coords or line.start > box.max_coords:
        return False
    elif line.start >= box.min_coords and line.end <= box.max_coords:
        return True
    
    overlapping_dims = 0
    overlapping_bounds = [0, 1]
    for i in range(line.dims):
        line_norm = line.end[i] - line.start[i]
        
        if abs(line_norm) < 1e-3 and box.min_coords[i] <= line.start[i] <= box.max_coords[i]:
            overlapping_dims += 1 # don't modify bounds
            continue

        intersection_start = 

        
        



def identify_intersection_bounding_boxes(line: Line, box: Box) -> bool:
    if line.dims != box.dims:
        raise ValueError("Line and Box dimensions must match.")

    # Work on a copy to avoid modifying the original line object
    clipped_line = copy.deepcopy(line)
    
    for i in range(line.dims):
        line_bounds = clipped_line.get_axis_bounds(i)
        box_bounds = box.get_bounds(i)

        # Check for no overlap
        if line_bounds[0] > box_bounds[1] or line_bounds[1] < box_bounds[0]:
            return False
        else:
            # Clip the line bounds to the box bounds
            clipped_line.set_axis_bounds(i, max(line_bounds[0], box_bounds[0]), min(line_bounds[1], box_bounds[1]))

    # Check if the resulting clipped line has any dimension with size > 0
    has_size = False
    for i in range(line.dims):
        if abs(clipped_line.end[i] - clipped_line.start[i]) > 0:
            has_size = True
            break
            
    if has_size:
        # Format output to match original style: "Start(x, y, ...), End(x, y, ...)"
        start_str = ", ".join(map(str, clipped_line.start))
        end_str = ", ".join(map(str, clipped_line.end))
        print(f"Clipped Line Coordinates: Start({start_str}), End({end_str})")
        return True

    return False

class TestIntersection(unittest.TestCase):

    def test_line_touches_cube_corner(self):
        print("\nTest 1: Line touches cube corner")
        test_line = Line(0, 0, 0, 1, 1, 1)
        test_cube = Box(1, 1, 1, 4, 4, 4)
        self.assertFalse(identify_intersection_bounding_boxes(test_line, test_cube))

    def test_line_inside_cube(self):
        print("\nTest 2: Line completely inside cube")
        test_line = Line(2, 2, 2, 3, 3, 3)
        test_cube = Box(1, 1, 1, 4, 4, 4)
        self.assertTrue(identify_intersection_bounding_boxes(test_line, test_cube))

    def test_line_outside_cube(self):
        print("\nTest 3: Line completely outside cube")
        test_line = Line(5, 5, 5, 6, 6, 6)
        test_cube = Box(1, 1, 1, 4, 4, 4)
        self.assertFalse(identify_intersection_bounding_boxes(test_line, test_cube))

    def test_line_goes_through_cube(self):
        print("\nTest 4: Line goes through cube")
        test_line = Line(0, 0, 0, 5, 5, 5)
        test_cube = Box(1, 1, 1, 4, 4, 4)
        self.assertTrue(identify_intersection_bounding_boxes(test_line, test_cube))

    def test_line_touches_square_corner(self):
        print("\nTest 1 (2D): Line touches square corner")
        test_line = Line(0, 0, 1, 1)
        test_square = Box(1, 1, 4, 4)
        self.assertFalse(identify_intersection_bounding_boxes(test_line, test_square))

    def test_line_inside_square(self):
        print("\nTest 2 (2D): Line completely inside square")
        test_line = Line(2, 2, 3, 3)
        test_square = Box(1, 1, 4, 4)
        self.assertTrue(identify_intersection_bounding_boxes(test_line, test_square))

    def test_line_outside_square(self):
        print("\nTest 3 (2D): Line completely outside square")
        test_line = Line(5, 5, 6, 6)
        test_square = Box(1, 1, 4, 4)
        self.assertFalse(identify_intersection_bounding_boxes(test_line, test_square))

    def test_line_crosses_square(self):
        print("\nTest 4 (2D): Line crosses square")
        test_line = Line(0, 0, 5, 5)
        test_square = Box(1, 1, 4, 4)
        self.assertTrue(identify_intersection_bounding_boxes(test_line, test_square))

    def test_line_bounding_box_overlaps_square_but_no_intersection(self):
        print("\nTest 5 (2D): Line bounding box overlaps square but no intersection")
        test_line = Line(0, 0, 5, 5)
        test_square = Box(0, 3, 1, 4)
        self.assertFalse(identify_intersection_bounding_boxes(test_line, test_square))

if __name__ == "__main__":
    unittest.main()
