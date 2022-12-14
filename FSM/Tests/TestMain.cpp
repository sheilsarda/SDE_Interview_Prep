#include "../GarageDoor.h"
#include "gtest/gtest.h"

TEST(instantiationTest, garageDoorTest)
{
    EXPECT_EQ(1000, 1000); 
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
