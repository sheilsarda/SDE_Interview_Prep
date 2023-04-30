#include "DPSoln.h"
using namespace std;

int testsToRun[1]; // idxs of tests to run (located in tests subdirectory)

string inputFile = "tests/test_input_";
string outputFile = "tests/cpp_test_output_";

int main(){

    cout << "Hello world\r\n";
    for(int testCase : testsToRun){

        DPGridTraversal dpSoln( inputFile + to_string(testCase), 
                                outputFile + to_string(testCase));
        dpSoln.findOptimalPath();

    }



}
