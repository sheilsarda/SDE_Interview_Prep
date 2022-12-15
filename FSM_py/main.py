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
        self.__current_state = DoorState['Closed']
        self.__prev_state = DoorState['Closed']
        self.__action_counter = 0
        self.currentTime = 0
        self.safetyTriggerActivated = False
        self.__doorOpenTime = 5
        self.__doorCloseTime = 5
        self.__userInput = ""
        self.__inputMutex = Lock()

    def doorTriggered(self): 
        if(DoorState['Closed'] == self.__curentState):
            self.__prevState = self.__curentState
            self.__curentState = DoorState['Start_Opening']
            self.__actionCounter = 0
        elif(DoorState['Open'] == self.__curentState):
            self.__prevState = self.__curentState
            self.__curentState = DoorState['Start_Closing']
            self.__actionCounter = 0
        elif(DoorState['Start_Opening'] == self.__curentState):
            self.__prevState = self.__curentState
            self.__curentState = DoorState['Freeze']
            self.__actionCounter = 0
        elif(DoorState['Start_Closing'] == self.__curentState):
            self.__prevState = self.__curentState
            if(self.safetyTriggerActivated):
                self.__curentState = DoorState['Start_Opening']
                self.__actionCounter = time()
            else:
                self.__curentState = DoorState['Freeze']
                self.__actionCounter = 0
        elif(DoorState['Freeze'] == self.__curentState):
            if(self.__prevState == DoorState['Start_Opening']):
                self.__curentState = DoorState['Start_Closing']
            else:
                self.__curentState = DoorState['Start_Opening']
            self.__actionCounter = time()
            self.__prevState = self.__curentState
        
        if(self.safetyTriggerActivated):
            if(self.__prevState == DoorState['Start_Closing']):
                print("Object Detected; Safety Trigger Activated\n")
            else: 
                print("Safety Trigger Cannot be activated unless door is closing")
            self.safetyTriggerActivated = False;
        
        print(self.__curentState.name)
        return self.__curentState

    def timerCompare(self):
        if(self.currentState == DoorState['Start_Opening']):
            timeAfterAction = self.__actionCounter + self.__doorOpenTime
            if(self.currentTime >= timeAfterAction):
                self.__currentState = DoorState['Open']
                self.__actionCounter = 0
                print(self.__curentState.name)
        return
    
    def printCurrentState(self):
        print(self.__curentState.name)


    async def getLine(self):
        consoleBuffer = await ainput(self.shell_prompt)
        await self.__inputMutex.acquire()
        self.__userInput = consoleBuffer
        self.__inputMutex.release()
        

async def main():
    print("Please type any keys + \"Enter\" to trigger garage door remote; \"exit\" to quite")
    door = GarageDoor()
    while True:
        door.currentTime = time()
        door.timerCompare()
        door.getLine()
        if(len(self.__userInput)):
            if(self.__userinput == "exit"): 
                break
            elif)self.__userInput

        


    return

if __name__ == "__main__":
    print("Hello world")
    main()
