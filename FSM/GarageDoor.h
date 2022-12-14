#ifndef GarageDoorClass
#define GarageDoorClass

#define doorCloseTime   5; // secs to close door
#define doorOpenTime    5; // secs to open door

#include <iostream>
#include <string>
#include <chrono>
#include <fcntl.h>
#include <iostream>
#include <thread>
#include <mutex>
#include <atomic>
#include <pthread.h>

using namespace std;

class GarageDoor {
    enum DoorState{
        Closed=0, 
        Open=1, 
        Start_Opening=2, 
        Start_Closing=3,
        Freeze=-1
    };

    private:
        volatile DoorState currentState, prevState;
        volatile time_t actionCounter;

    public:
        volatile time_t currentTime;
        volatile bool safetyTriggerActivated;
        GarageDoor();
        ~GarageDoor();
        DoorState doorTriggered();
        DoorState safetyTrigger();
        void timerCompare();
        string printCurrentState();
};

class GetLineThread {
    private:
        atomic<bool> fetchingInput, sendOverInput; 
        string input;
        mutex inputLock; // Mutex to permit only one thread to acceses input (processor vs. fetcher)

    public:
        GetLineThread();
        ~GetLineThread();
        string GetLine();
};


#endif /* GarageDoorClass */

