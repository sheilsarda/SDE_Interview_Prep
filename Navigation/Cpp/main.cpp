#include "DPSoln.h"
using namespace std;

int main(){

    string inputFile = "../Python/tests/test_input_1.txt";
    string outputFile = "test_output_1.txt";

    cout << "Hello world\r\n";
    DPGridTraversal dpSoln(inputFile, outputFile);

    dpSoln.findOptimalPath();




}
