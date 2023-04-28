#ifndef DPSoln
#define DPSoln

#include <iostream>
#include <string>
#include <chrono>
#include <fstream>
#include <vector>



using namespace std;

class DPGridTraversal {


    private:
        string inputFileName, outputFileName;
        vector<vector<char>> maze;
        vector<pair<int, int>>  avocadoPositions;

        int robotRow, robotCol;


    public:
        DPGridTraversal(string, string);
        ~DPGridTraversal();


};


#endif 

