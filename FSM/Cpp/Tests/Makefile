CXX = g++
CXXFLAGS = -std=c++17 -Wall -I h -I /usr/local/include/gtest/ -c
LXXFLAGS = -std=c++17 -I h -pthread
OBJECTS = program.o main.o 
GTEST = /usr/local/lib/libgtest.a
TARGET = main

$(TARGET): $(OBJECTS)
	$(CXX) $(LXXFLAGS) -o $(TARGET) $(OBJECTS) $(GTEST)

program.o: ../GarageDoor.cpp
	$(CXX) $(CXXFLAGS) ../GarageDoor.cpp -o program.o
main.o: TestMain.cpp
	$(CXX) $(CXXFLAGS) TestMain.cpp -o main.o
clean:
	rm -fv $(TARGET) $(OBJECTS)