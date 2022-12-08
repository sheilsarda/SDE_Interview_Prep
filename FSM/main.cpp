#include "GarageDoor.h"

GarageDoor::GarageDoor():currentState(Closed), prevState(Closed) {
}

GarageDoor::DoorState GarageDoor::doorTriggered(){
    return GarageDoor::currentState;
}
GarageDoor::DoorState GarageDoor::safetyTrigger(){
    return GarageDoor::currentState;
}
