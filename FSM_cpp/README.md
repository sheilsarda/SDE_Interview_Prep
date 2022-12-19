# CPP Solution Docs

- Compile / build program by running `make all` in the directory containing `main.cpp`; this step assumes you have `C++` build tools installed (`C++17` preferred)
- Run program `garageDoor` from the command line through `./garageDoor`
- Input trigger for the garage door remote can be provided by typing any character or sequence on your keyboard and hitting `Enter`
- Safety function can be triggered by typing `safety` in the command line as the door is closing 
- Exit loop/program by typing `exit` in the command line

## How to run test cases

- Navigate to `Tests` directory
- Make sure you have Google's C++ Test suite installed to run test cases; setup guide can be found [here](https://google.github.io/googletest/quickstart-cmake.html)
- Run `make` to generate test case executable `main`, which can be run by executing `./main` 
- You should get the below outcome with 4/4 test cases passing

![](CPP_Test_cases.jpg)