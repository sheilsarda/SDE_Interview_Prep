import unittest
from main import *
from time import sleep, time

class Test_Garage_Door(unittest.TestCase):

    def test_door_trigger(self):
        door = Garage_door()
        door.door_triggered()
        sleep(7)
        door.current_time = time()
        door.timer_compare()
        self.assertEqual(door.print_current_state(), 'Open')
    
    def test_door_freeze(self):
        door = Garage_door()
        door.door_triggered()
        door.current_time = time()
        sleep(2)
        door.current_time = time()
        door.timer_compare()
        door.door_triggered()

        self.assertEqual(door.print_current_state(), 'Freeze')

if __name__ == '__main__':
    unittest.main()