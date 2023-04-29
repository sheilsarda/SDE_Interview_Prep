#ifndef DPSoln
#define DPSoln

#include <iostream>
#include <string>
#include <chrono>
#include <fstream>
#include <vector>
#include <queue>
#include <set>


using namespace std;

class DPGridTraversal {


    private:
        string inputFileName, outputFileName;
        vector<vector<char>> maze;
        vector<pair<int, int>>  avocadoPositions;

        int robotRow, robotCol;

        void buildDistanceMatrix();

    public:
        DPGridTraversal(string, string);
        ~DPGridTraversal();

        vector<vector<int>> bfs(int, int);


};


#endif 

