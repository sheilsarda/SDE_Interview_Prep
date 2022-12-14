from enum import Enum

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
        self.currentTime = 
        self.safetyTriggerActivated = False

    def doorTriggered(self): 
        return
    
    def safetyTrigger(self):
        return

    def timerCompare(self):
        return
    
    def printCurrentState(self):
        print(self.currentState.name)