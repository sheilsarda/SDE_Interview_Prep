#ifndef GarageDoorClass
#define GarageDoorClass

class GarageDoor {
    enum DoorState{
        Closed=0, 
        Open=1, 
        Start_Opening=2, 
        Start_Closing=3
    };

    private:
        DoorState currentState, prevState;

    public:
        GarageDoor();
        DoorState doorTriggered();
        DoorState safetyTrigger();

};

#endif /* GarageDoorClass */
