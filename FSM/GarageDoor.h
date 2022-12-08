#ifndef GarageDoorClass
#define GarageDoorClass

#define doorCloseTime   15000; // milliseconds to close door
#define doorOpenTime    15000; // milliseconds to open door

class GarageDoor {
    enum DoorState{
        Closed=0, 
        Open=1, 
        Start_Opening=2, 
        Start_Closing=3,
        Freeze=-1
    };

    private:
        DoorState currentState, prevState;
        unsigned int actionCounter, currentTime;

    public:
        GarageDoor();
        DoorState doorTriggered();
        DoorState safetyTrigger();
        void timerCompare();

};

#endif /* GarageDoorClass */
