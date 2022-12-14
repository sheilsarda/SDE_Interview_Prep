CXX = g++
CXXFLAGS = -std=c++17 -Wall -I h -I /usr/local/include/gtest/ -c
LXXFLAGS = -std=c++17 -I h -pthread
OBJECTS = program.o main.o program_unittest.o
GTEST = /usr/local/lib/libgtest.a
TARGET = main

$(TARGET): $(OBJECTS)
	$(CXX) $(LXXFLAGS) -o $(TARGET) $(OBJECTS) $(GTEST)

program.o: ../GarageDoor.cpp
	$(CXX) $(CXXFLAGS) ../GarageDoor.cpp -o program.o
program_unittest.o: GarageDoorTest.cpp
	$(CXX) $(CXXFLAGS) GarageDoorTest.cpp -o program_unittest.o
main.o: TestMain.cpp
	$(CXX) $(CXXFLAGS) TestMain.cpp -o main.o
clean:
	rm -fv $(TARGET) $(OBJECTS)