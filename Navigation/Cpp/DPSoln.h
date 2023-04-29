#ifndef DPSoln
#define DPSoln

#include <iostream>
#include <string>
#include <chrono>
#include <fstream>
#include <vector>
#include <queue>
#include <set>
#include <tuple>


using namespace std;

class DPGridTraversal {


    private:
        string inputFileName, outputFileName;
        vector<vector<char>> maze;
        vector<pair<int, int>>  avocadoPositions;

        int robotRow, robotCol;

        void buildDistanceMatrix();
        vector<vector<int>> bfs(int, int);

    public:
        DPGridTraversal(string, string);
        ~DPGridTraversal();



};


#endif 

