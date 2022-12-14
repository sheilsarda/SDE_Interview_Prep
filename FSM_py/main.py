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
            self.prevState = self.currentState
            self.currentState = DoorState['Start_Opening']
            self.actionCounter = 0
        elif(DoorState['Open'] == self.currentState):
            self.prevState = self.currentState
            self.currentState = DoorState['Start_Closing']
            self.actionCounter = 0
        elif(DoorState['Start_Opening'] == self.currentState):
            self.prevState = self.currentState
            self.currentState = DoorState['Freeze']
            self.actionCounter = 0
        elif(DoorState['Start_Closing'] == self.currentState):
            self.prevState = self.currentState
            if(self.safetyTriggerActivated):
                self.currentState = DoorState['Start_Opening']
                self.actionCounter = time()
            else:
                self.currentState = DoorState['Freeze']
                self.actionCounter = 0
        elif(DoorState['Freeze'] == self.currentState):
            if(self.prevState == DoorState['Start_Opening']):
                self.currentState = DoorState['Start_Closing']
            else:
                self.currentState = DoorState['Start_Opening']
            self.actionCounter = time()
            self.prevState = self.currentState
        
        


    def safetyTrigger(self):
        return

    def timerCompare(self):
        return
    
    def printCurrentState(self):
        print(self.currentState.name)