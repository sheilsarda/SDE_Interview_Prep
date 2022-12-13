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

        } while (fetchingInput && input != "exit");

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
        cout << returnInput << "\r\n";
        return returnInput;
    }
}

/// @brief Destructor
GarageDoor::~GarageDoor() { }

/// @brief Constructor using initializer list
GarageDoor::GarageDoor():currentState(Closed), prevState(Closed), 
    actionCounter(0), currentTime(0) {
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

/// @brief update state if door has finished opening or closing
void GarageDoor::timerCompare(){
    time_t timeAfterAction;
    switch(GarageDoor::currentState){
        case Start_Opening:
            timeAfterAction = ((int) GarageDoor::actionCounter) + 5;
            if(timeAfterAction <= currentTime){
                GarageDoor::currentState    = Open;
                GarageDoor::actionCounter   = 0;
                cout << printState(currentState) << "\r\n";
            } 
            break;
        case Start_Closing:
            timeAfterAction = GarageDoor::actionCounter + 5;
            if(timeAfterAction <= currentTime){
                GarageDoor::currentState    = Closed;
                GarageDoor::actionCounter   = 0;
                cout << printState(currentState) << "\r\n";
            }
    }
}

/// @brief converts enum of door state to a string that can be printed on cout
/// @param state : current garage door state
/// @return returns string representation of state
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
    cout << "Please press any key to trigger garage door remote; \"exit\"" <<
                " to exit loop\r\n";
    GarageDoor door;
    GetLineThread inputFetcher;
    string input = "";

    for(;;){
        door.currentTime = chrono::system_clock::to_time_t(
            chrono::system_clock::now());
        door.timerCompare();
        
        input = inputFetcher.GetLine();
        if (!input.empty()) {
            cout << "Door Triggered at " << door.currentTime << "seconds \r\n";
            cout << door.doorTriggered() << "\r\n";
        }
    }
}
