#include "DPSoln.h"
using namespace std;

int testsToRun[] = {1, 2, 3, 4, 5}; // idxs of tests to run (located in tests subdirectory)

string inputFile = "../tests/test_input_";
string outputFile = "../tests/cpp_test_output_";

int main(){

    for(int testCase : testsToRun){
        string inputFileTest = inputFile + to_string(testCase) + ".txt";
        string outputFileTest = outputFile + to_string(testCase) + ".txt";

        cout << "Starting test " << to_string(testCase) << endl;
        cout << "Input file name: " << inputFileTest << endl;

        DPGridTraversal dpSoln( inputFileTest, outputFileTest);
        dpSoln.findOptimalPath();

        cout << "Finished running test " << to_string(testCase) << endl;

    }
}
