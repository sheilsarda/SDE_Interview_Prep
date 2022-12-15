#include "GarageDoor.h"
using namespace std;

int main(){
    cout << "Please type any keys + \"Enter\" to trigger garage door remote; \"exit\"" <<
                " to quite\r\n";
    GarageDoor door;
    GetLineThread inputFetcher;
    string input = "";

    for(;;){
        door.currentTime = chrono::system_clock::to_time_t(
            chrono::system_clock::now());
        door.timerCompare();
        
        input = inputFetcher.GetLine();
        if (!input.empty()) {
            if(input == "exit") break;
            
            if(input == "safety") door.safetyTriggerActivated = true;
            else cout << "Door Triggered at " << door.currentTime << "seconds \r\n";

            door.doorTriggered();
        }
    }
    inputFetcher.~GetLineThread();
}
