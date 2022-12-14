#include "GarageDoor.h"
using namespace std;

/// @brief Constructor which initializes new thread 
GetLineThread::GetLineThread() {
    input = "";
    sendOverInput = true;
    fetchingInput = true;
    
    thread([&](){
        string inputBuffer; 
        char charReceived;
        
        do {
            inputBuffer = "";
            while (fetchingInput) {
                // Non-blocking wait
                while (cin.peek() == EOF) this_thread::yield(); 
                charReceived = cin.get();
                if (charReceived == '\n') break;
                inputBuffer += charReceived;
            }

            // Non-blocking wait for processing thread to free up to receive
            if (!fetchingInput) break;
            while (fetchingInput && !sendOverInput) this_thread::yield();
            if (!fetchingInput) break;

            // Safely sync thread input with processor input string
            inputLock.lock(); 
            input = inputBuffer; 
            inputLock.unlock();

            // Don't send next line until the processing thread is ready
            sendOverInput = false;

        } while (fetchingInput);

    }).detach();
}

/// @brief Destructor; stops fetcher thread
GetLineThread::~GetLineThread() {
    fetchingInput = false; 
}

/// @brief Get next line 
/// @return returns string input if ready; else, empty string.
string GetLineThread::GetLine() {
    if (sendOverInput) return "";
    else {
        // Retrieve next line from fetcher thread and store for return
        inputLock.lock();
        string returnInput = input;
        inputLock.unlock();

        // Signal to fetcher that it can continue sending over next line if available
        sendOverInput = true; 
        return returnInput;
    }
}

/// @brief Destructor
GarageDoor::~GarageDoor() { }

/// @brief Constructor using initializer list
GarageDoor::GarageDoor():currentState(Closed), prevState(Closed), 
    actionCounter(0), currentTime(0), safetyTriggerActivated(false) {
}

/// @brief Constructor used for testing various start configurations
GarageDoor::GarageDoor(DoorState ds):currentState(ds), prevState(Closed), 
    actionCounter(0), currentTime(0), safetyTriggerActivated(false) {
}

/// @brief update FSM when door is triggered
/// @return current state after update
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
            GarageDoor::currentState = Freeze;   
            GarageDoor::actionCounter   = 0; 
            break;            
        case Start_Closing:
            GarageDoor::prevState       = Start_Closing;
            if(safetyTriggerActivated) {
                GarageDoor::currentState = Start_Opening;  
                GarageDoor::actionCounter   = GarageDoor::currentTime;
            } else {
                GarageDoor::currentState    = Freeze;  
                GarageDoor::actionCounter   = 0; 
            }
            break;            
        case Freeze:
            if(GarageDoor::prevState == Start_Opening) 
                GarageDoor::currentState = Start_Closing;
            else GarageDoor::currentState   = Start_Opening;
            GarageDoor::actionCounter       = GarageDoor::currentTime;
            GarageDoor::prevState           = Freeze;
    }
    if(safetyTriggerActivated){
        if(GarageDoor::prevState == Start_Closing)
            cout << "Object detected; Safety Trigger activated" << "\r\n";
        else cout << "Safety Trigger cannot be activated unless door is closing" << "\r\n";
        safetyTriggerActivated = false;
    }
    cout << printCurrentState() << "\r\n";
    return GarageDoor::currentState;
}
GarageDoor::DoorState GarageDoor::safetyTrigger(){
    return GarageDoor::currentState;
}

/// @brief update state if door has finished opening or closing
void GarageDoor::timerCompare(){
    time_t timeAfterAction;
    switch(GarageDoor::currentState){
        case Start_Opening:
            timeAfterAction = ((int) GarageDoor::actionCounter) + doorOpenTime;
            if(timeAfterAction <= currentTime){
                GarageDoor::currentState    = Open;
                GarageDoor::actionCounter   = 0;
                cout << printCurrentState() << "\r\n";
            } 
            break;
        case Start_Closing:
            timeAfterAction = GarageDoor::actionCounter + doorCloseTime;
            if(timeAfterAction <= currentTime){
                GarageDoor::currentState    = Closed;
                GarageDoor::actionCounter   = 0;
                cout << printCurrentState() << "\r\n";
            }
        default: return;
    }
}

/// @brief converts enum of door state to a string that can be printed on cout
/// @return returns string representation of current state
string GarageDoor::printCurrentState(){
    switch(GarageDoor::currentState){
        case Closed: return "Closed";
        case Open: return "Open"; 
        case Start_Opening: return "Starting to Open"; 
        case Start_Closing: return "Starting to Close"; 
        default: return "Freeze"; 
    }
}
