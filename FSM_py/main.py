from enum import Enum
from time import time

class DoorState(Enum):
    Closed=0
    Open=1
    Start_Opening=2,
    Start_Closing=3
    Freeze=-1

class GarageDoor(): 
    def __init__(self): 
        self.__currentState = DoorState['Closed']
        self.__prevState = DoorState['Closed']
        self.__actionCounter = 0
        self.currentTime = 0
        self.safetyTriggerActivated = False
        self.__doorOpenTime = 5
        self.__doorCloseTime = 5

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

def main():
    return

if __name__ == "__main__":
    print("Hello world")
    main()
