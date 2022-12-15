from enum import Enum
from time import time
from aioconsole import ainput
from asyncio import run
from threading import Lock

class Door_state(Enum):
    Closed=0
    Open=1
    Start_Opening=2,
    Start_Closing=3
    Freeze=-1

class Garage_door(): 
    def __init__(self): 
        self.__current_state = Door_state['Closed']
        self.__prev_state = Door_state['Closed']
        self.__action_counter = 0
        self.__door_open_time = 5
        self.__door_close_time = 5
        
        self.user_input = ""
        self.input_mutex = Lock()
        self.current_time = 0
        self.safety_trigger_activated = False

    def door_triggered(self): 
        if(Door_state['Closed'] == self.__current_state):
            self.__prev_state = self.__current_state
            self.__current_state = Door_state['Start_Opening']
            self.__action_counter = 0
        elif(Door_state['Open'] == self.__current_state):
            self.__prev_state = self.__current_state
            self.__current_state = Door_state['Start_Closing']
            self.__action_counter = 0
        elif(Door_state['Start_Opening'] == self.__current_state):
            self.__prev_state = self.__current_state
            self.__current_state = Door_state['Freeze']
            self.__action_counter = 0
        elif(Door_state['Start_Closing'] == self.__current_state):
            self.__prev_state = self.__current_state
            if(self.safety_trigger_activated):
                self.__current_state = Door_state['Start_Opening']
                self.__action_counter = time()
            else:
                self.__current_state = Door_state['Freeze']
                self.__action_counter = 0
        elif(Door_state['Freeze'] == self.__current_state):
            if(self.__prev_state == Door_state['Start_Opening']):
                self.__current_state = Door_state['Start_Closing']
            else:
                self.__current_state = Door_state['Start_Opening']
            self.__action_counter = time()
            self.__prev_state = self.__current_state
        
        if(self.safety_trigger_activated):
            if(self.__prev_state == Door_state['Start_Closing']):
                print("Object Detected; Safety Trigger Activated\n")
            else: 
                print("Safety Trigger Cannot be activated unless door is closing")
            self.safety_trigger_activated = False;
        
        print(self.__current_state.name)
        return self.__current_state

    def timer_compare(self):
        if(self.__current_state == Door_state['Start_Opening']):
            time_after_action = self.__action_counter + self.__door_open_time
            if(self.currentTime >= time_after_action):
                self.__current_state = Door_state['Open']
                self.__action_counter = 0
                print(self.__current_state.name)
        elif(self.__current_state == Door_state['Start_Closing']):
            time_after_action = self.__action_counter + self.__door_close_time
            if(self.currentTime >= time_after_action):
                self.__current_state = Door_state['Closed']
                self.__action_counter = 0
        print(self.__current_state.name)
        return
    
    def printCurrentState(self):
        print(self.__current_state.name)

    async def get_console_line(self):
        consoleBuffer = await ainput()
        while(self.input_mutex.locked()): 
            continue
        self.input_mutex.acquire()
        self.user_input = consoleBuffer
        self.input_mutex.release()
        

async def main():
    print("Please type any keys + \"Enter\" to trigger garage door remote; \"exit\" to quite")
    door = Garage_door()
    while True:
        door.current_time = time()
        door.timer_compare()
        await door.get_console_line()
        if(len(door.user_input)):
            if(door.user_input == "exit"): 
                break
            elif(door.user_input == "safety"):
                door.safety_trigger_activated = True
            else:
                print("Door triggered at ",door.current_time,"seconds")
            door.doorTriggered()
        while(door.input_mutex.locked()): 
            continue 
        door.input_mutex.acquire()
        door.user_input = ""
        door.input_mutex.release()
    
    return

if __name__ == "__main__":
    print("Hello world")
    run(main())
