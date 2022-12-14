#include "../GarageDoor.h"
#include "gtest/gtest.h"

using namespace std;

TEST(instantiationTest, garageDoorTest)
{
    GarageDoor door;
    door.currentTime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    door.doorTriggered();

    std::this_thread::sleep_for(chrono_literals:7s);
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
