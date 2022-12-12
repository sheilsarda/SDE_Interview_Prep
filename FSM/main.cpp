#include "GarageDoor.h"

using namespace std;

// https://stackoverflow.com/questions/16592357/non-blocking-stdgetline-exit-if-no-input
class AsyncGetline {
    public:
        //AsyncGetline is a class that allows for asynchronous CLI getline-style input
        AsyncGetline() {
            input = "";
            sendOverNextLine = true;
            continueGettingInput = true;

            thread([&](){
                //Start a new detached thread to call getline over and over again and retrieve new input to be processed.
                string synchronousInput;
                char nextCharacter;
                do {
                    //Get the asynchronous input lines.
                    synchronousInput = "";
                    while (continueGettingInput) {
                        while (cin.peek() == EOF) {
                            //Ensure that the other thread is always yielded to when necessary. Don't sleep here;
                            //only yield, in order to ensure that processing will be as responsive as possible.
                            this_thread::yield();
                        }
                        nextCharacter = cin.get();
                        if (nextCharacter == '\n') break;
                        synchronousInput += nextCharacter;
                    }

                    if (!continueGettingInput) break;

                    //Wait until the processing thread is ready to process the next line.
                    while (continueGettingInput && !sendOverNextLine) {
                        //Ensure that the other thread is always yielded to when necessary. Don't sleep here;
                        //only yield, in order to ensure that the processing will be as responsive as possible.
                        this_thread::yield();
                    }

                    if (!continueGettingInput) break;

                    //Safely send the next line of input over for usage in the processing thread.
                    inputLock.lock(); input = synchronousInput; inputLock.unlock();

                    //Signal that although this thread will read in the next line,
                    //it will not send it over until the processing thread is ready.
                    sendOverNextLine = false;
                }
                while (continueGettingInput && input != "exit");
            }).detach();
        }

        ~AsyncGetline() {
            continueGettingInput = false; //Stop the getline thread.
        }

        //Get the next line of input if there is any; if not, sleep for a millisecond and return an empty string.
        string GetLine() {
            //See if the next line of input, if any, is ready to be processed.
            if (sendOverNextLine) {
                //Don't consume the CPU while waiting for input; this_thread::yield()
                //would still consume a lot of CPU, so sleep must be used.
                this_thread::sleep_for(chrono::milliseconds(1));
                return "";
            }
            else {
                //Retrieve the next line of input from the getline thread and store it for return.
                inputLock.lock();
                string returnInput = input;
                inputLock.unlock();

                //Also, signal to the getline thread that it can continue
                //sending over the next line of input, if available.
                sendOverNextLine = true;
                return returnInput;
            }
        }

    private:
        //Cross-thread-safe boolean to tell the getline thread to stop when AsyncGetline is deconstructed.
        atomic<bool> continueGettingInput;

        //Cross-thread-safe boolean to denote when the processing thread is ready for the next input line.
        //This exists to prevent any previous line(s) from being overwritten by new input lines without
        //using a queue by only processing further getline input when the processing thread is ready.
        atomic<bool> sendOverNextLine;

        //Mutex lock to ensure only one thread (processing vs. getline) is accessing the input string at a time.
        mutex inputLock;

        //string utilized safely by each thread due to the inputLock mutex.
        string input;
};

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
            timeAfterAction = ((int) GarageDoor::actionCounter) + 5000;
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
                " to exit loop\r\n";
    GarageDoor door;
    AsyncGetline getLineObj;
    string input = "";

    for(;;){
        door.currentTime = chrono::system_clock::to_time_t(
            chrono::system_clock::now());
        door.timerCompare();
        
        input = getLineObj.GetLine();
        if (!input.empty()) {
            getline(cin, input);
            cout << "Door Triggered at " << door.currentTime << "seconds \r\n";
            cout << door.doorTriggered() << "\r\n";
        }
    }
}
