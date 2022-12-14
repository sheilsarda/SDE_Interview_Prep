#include "../GarageDoor.h"
#include "gtest/gtest.h"

using namespace std;

TEST(doorTriggerTest1, garageDoorTests)
{
    using namespace std::chrono_literals;
    GarageDoor door;
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.doorTriggered();

    std::this_thread::sleep_for(7s);
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.timerCompare();
        
    EXPECT_EQ(door.printCurrentState(), "Open"); 
}

TEST(doorTriggerTest2, garageDoorTests)
{
    using namespace std::chrono_literals;
    GarageDoor door(DoorState::Open);
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.doorTriggered();

    std::this_thread::sleep_for(7s);
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.timerCompare();
        
    EXPECT_EQ(door.printCurrentState(), "Closed"); 
}

TEST(doorTriggerTest3, garageDoorTests)
{
    using namespace std::chrono_literals;
    GarageDoor door(Open);
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.doorTriggered();

    std::this_thread::sleep_for(2s);
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.timerCompare();

    door.doorTriggered();
    EXPECT_EQ(door.printCurrentState(), "Freeze"); 
}

TEST(doorTriggerTest4, garageDoorTests)
{
    using namespace std::chrono_literals;
    GarageDoor door(Freeze);
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.doorTriggered();
    std::this_thread::sleep_for(7s);
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.timerCompare();

    EXPECT_EQ(door.printCurrentState(), "Open"); 
}

int main(int argc, char **argv)
{
    ::testing::InitGoogleTest(&argc, argv);
    std::cout << "RUNNING TESTS ..." << std::endl;
    int ret{RUN_ALL_TESTS()};
    if (!ret)
        std::cout << "<<<SUCCESS>>>" << std::endl;
    else
        std::cout << "FAILED" << std::endl;
    return 0;
}
