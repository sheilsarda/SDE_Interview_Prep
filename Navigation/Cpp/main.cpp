#include "DPSoln.h"
using namespace std;

int testsToRun[] = {1, 2, 3, 4, 5}; // idxs of tests to run (located in tests subdirectory)

string inputFile = "../tests/test_input_";
string outputFile = "../tests/cpp_test_output_";

int main(){

    for(int testCase : testsToRun){
        cout << "Hello world\r\n";
        string inputFileTest = inputFile + to_string(testCase) + ".txt";
        string outputFileTest = outputFile + to_string(testCase) + ".txt";

        cout << "Input file name: " << inputFileTest << endl;


        DPGridTraversal dpSoln( inputFileTest, outputFileTest);
        dpSoln.findOptimalPath();

    }



}
