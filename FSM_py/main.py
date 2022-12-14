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
        self.currentState = DoorState['Closed']
        self.prevState = DoorState['Closed']
        self.actionCounter = 0
        self.currentTime = 0
        self.safetyTriggerActivated = False

    def doorTriggered(self): 
        if(DoorState['Closed'] == self.currentState):
            return
        elif(DoorState['Closed'] == self.currentState):
            return
        elif(DoorState['Start_Opening'] == self.currentState):
            return
        elif(DoorState['Start_Closing'] == self.currentState):
            return
        elif(DoorState['Freeze'] == self.currentState):
            return

    def safetyTrigger(self):
        return

    def timerCompare(self):
        return
    
    def printCurrentState(self):
        print(self.currentState.name)