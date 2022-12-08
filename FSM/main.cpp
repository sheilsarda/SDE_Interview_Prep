#include "GarageDoor.h"
#include <iostream>

GarageDoor::GarageDoor():currentState(Closed), prevState(Closed), actionCounter(0) {
}

GarageDoor::DoorState GarageDoor::doorTriggered(){
    switch(GarageDoor::currentState){
        case Closed: 
            GarageDoor::prevState       = Closed;
            GarageDoor::currentState    = Start_Opening;
            GarageDoor::actionCounter   = GarageDoor::currentTime;
            break;
        case Open:
            GarageDoor::prevState       = Open;
            GarageDoor::currentState    = Start_Closing;
            GarageDoor::actionCounter   = GarageDoor::currentTime;
            break;            
        case Start_Opening:
            GarageDoor::prevState       = Start_Opening;
            GarageDoor::currentState    = Freeze;   
            GarageDoor::actionCounter   = 0; 
            break;            
        case Start_Closing:
            GarageDoor::prevState       = Start_Closing;
            GarageDoor::currentState    = Freeze;  
            GarageDoor::actionCounter   = 0; 
            break;            
        case Freeze:
            if(GarageDoor::prevState == Start_Opening) GarageDoor::currentState = Start_Closing;
            else GarageDoor::currentState = Start_Opening;
            GarageDoor::actionCounter   = GarageDoor::currentTime;
            GarageDoor::prevState       = Freeze;
    }
    return GarageDoor::currentState;
}
GarageDoor::DoorState GarageDoor::safetyTrigger(){
    return GarageDoor::currentState;
}

void GarageDoor::timerCompare(){
}


int main(){
    std::cout << "Hello World\r\n";
    GarageDoor door;
    
    std::cout << door.doorTriggered() << "\r\n";
}