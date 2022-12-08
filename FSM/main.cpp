#include "GarageDoor.h"
#include <iostream>

GarageDoor::GarageDoor():currentState(Closed), prevState(Closed) {
}

GarageDoor::DoorState GarageDoor::doorTriggered(){
    return GarageDoor::currentState;
}
GarageDoor::DoorState GarageDoor::safetyTrigger(){
    return GarageDoor::currentState;
}

int main(){
    std::cout << "Hello World\r\n";
}