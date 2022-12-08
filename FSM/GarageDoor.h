#ifndef GarageDoorClass
#define GarageDoorClass

enum DoorState {Open, Closed, Start_Opening, Start_Closing}

class GarageDoor {
    private:
        DoorState currentState;

    public:
        GarageDoor();
        doorTriggered();
        safetyTrigger();

}

#endif /* GarageDoorClass */
