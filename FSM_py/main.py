from enum import Enum
from time import time
from aioconsole import ainput
from threading import Thread, Lock

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
        self.current_time = 0
        self.safety_trigger_activated = False
        self.__door_open_time = 5
        self.__door_close_time = 5
        self.__user_input = ""
        self.__inputMutex = Lock()

    def doorTriggered(self): 
        if(Door_state['Closed'] == self.__current_state):
            self.__prevState = self.__current_state
            self.__current_state = Door_state['Start_Opening']
            self.__action_counter = 0
        elif(Door_state['Open'] == self.__current_state):
            self.__prevState = self.__current_state
            self.__current_state = Door_state['Start_Closing']
            self.__action_counter = 0
        elif(Door_state['Start_Opening'] == self.__current_state):
            self.__prevState = self.__current_state
            self.__current_state = Door_state['Freeze']
            self.__action_counter = 0
        elif(Door_state['Start_Closing'] == self.__current_state):
            self.__prevState = self.__current_state
            if(self.safetyTriggerActivated):
                self.__current_state = Door_state['Start_Opening']
                self.__action_counter = time()
            else:
                self.__current_state = Door_state['Freeze']
                self.__action_counter = 0
        elif(Door_state['Freeze'] == self.__current_state):
            if(self.__prevState == Door_state['Start_Opening']):
                self.__current_state = Door_state['Start_Closing']
            else:
                self.__current_state = Door_state['Start_Opening']
            self.__action_counter = time()
            self.__prevState = self.__current_state
        
        if(self.safetyTriggerActivated):
            if(self.__prevState == Door_state['Start_Closing']):
                print("Object Detected; Safety Trigger Activated\n")
            else: 
                print("Safety Trigger Cannot be activated unless door is closing")
            self.safetyTriggerActivated = False;
        
        print(self.__current_state.name)
        return self.__current_state

    def timerCompare(self):
        if(self.currentState == Door_state['Start_Opening']):
            timeAfterAction = self.__action_counter + self.__doorOpenTime
            if(self.currentTime >= timeAfterAction):
                self.__current_state = Door_state['Open']
                self.__action_counter = 0
                print(self.__current_state.name)
        return
    
    def printCurrentState(self):
        print(self.__current_state.name)


    async def getLine(self):
        consoleBuffer = await ainput(self.shell_prompt)
        await self.__inputMutex.acquire()
        self.__user_input = consoleBuffer
        self.__inputMutex.release()
        

async def main():
    print("Please type any keys + \"Enter\" to trigger garage door remote; \"exit\" to quite")
    door = GarageDoor()
    while True:
        door.currentTime = time()
        door.timerCompare()
        door.getLine()
        if(len(door.__user_input)):
            if(door.__user_input == "exit"): 
                break
            elif(door.__user_input == "safety"):
                door.safety_trigger_activated = True
            else:
                print("Door triggered at ",door.current_time,"seconds")
            door.doorTriggered()
        await self.__inputMutex.acquire()
        self.__user_input = ""
        self.__inputMutex.release()
    

        


    return

if __name__ == "__main__":
    print("Hello world")
    main()
