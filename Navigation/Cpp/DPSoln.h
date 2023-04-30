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
#include <unordered_map>
#include <algorithm>
#include <utility>
#include <numeric>
#include <bitset>

using namespace std;

class DPGridTraversal {


    private:
        string inputFileName, outputFileName;
        vector<vector<char>> maze;
        vector<pair<int, int>>  avocadoPositions;
        vector<vector<int>> distanceMat;

        int robotRow, robotCol;

        void buildDistanceMatrix();
        vector<vector<int>> bfs(int, int);
        vector<vector<int>> combinations(vector<int>, int);

    public:
        DPGridTraversal(string, string);
        ~DPGridTraversal();
        pair<int, vector<pair<int, int>>> findOptimalPath();

};


#endif 

