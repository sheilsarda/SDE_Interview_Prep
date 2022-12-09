#include "GarageDoor.h"

using namespace std;

GarageDoor::GarageDoor():currentState(Closed), prevState(Closed), 
    actionCounter(0), currentTime(0) {
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
            if(GarageDoor::prevState == Start_Opening) 
                GarageDoor::currentState = Start_Closing;
            else GarageDoor::currentState   = Start_Opening;
            GarageDoor::actionCounter       = GarageDoor::currentTime;
            GarageDoor::prevState           = Freeze;
    }
    cout << printState(GarageDoor::currentState) << "\r\n";
    return GarageDoor::currentState;
}
GarageDoor::DoorState GarageDoor::safetyTrigger(){
    return GarageDoor::currentState;
}

void GarageDoor::timerCompare(){
    time_t timeAfterAction;
    switch(GarageDoor::currentState){
        case Start_Opening:
            timeAfterAction = GarageDoor::currentTime + doorOpenTime;
            if(timeAfterAction <= currentTime){
                GarageDoor::currentState    = Open;
                GarageDoor::actionCounter   = 0;
                cout << printState(currentState) << "\r\n";
            } 
            break;
        case Start_Closing:
            timeAfterAction = GarageDoor::currentTime + doorCloseTime;
            if(timeAfterAction <= currentTime){
                GarageDoor::currentState    = Closed;
                GarageDoor::actionCounter   = 0;
                cout << printState(currentState) << "\r\n";
            }
    }
}

string GarageDoor::printState(DoorState state){
    switch(state){
        case Closed: return "Closed";
        case Open: return "Open"; 
        case Start_Opening: return "Starting to Open"; 
        case Start_Closing: return "Starting to Close"; 
        default: return "Freeze"; 
    }
}

int main(){
    int flags = fcntl(0, F_GETFL, 0);
    fcntl(0, F_SETFL, flags | O_NONBLOCK);

    cout << "Hello World\r\n";
    cout << "Please press any key to trigger garage door remote; \"exit\"" <<
                "to exit loop\r\n";
    GarageDoor door;
    string input;

    for(;;){
        door.currentTime = chrono::system_clock::to_time_t(
            chrono::system_clock::now());
        door.timerCompare();
        getline(cin, input);
        if(input.compare("\n")) continue;
        else {
            cout << "Door Triggered at " << door.currentTime << "seconds \r\n";
            cout << door.doorTriggered() << "\r\n";
            if(input == "exit") break;
        }
    }
}
