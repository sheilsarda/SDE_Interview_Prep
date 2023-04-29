#include "DPSoln.h"
using namespace std;



/// @brief Destructor
DPGridTraversal::~DPGridTraversal() { }

/// @brief Constructor using initializer list
DPGridTraversal::DPGridTraversal(string inputFile, string outputFile) : inputFileName(inputFile), 
    outputFileName(outputFile) {

    ifstream f(this->inputFileName);
    string line;
    
    while (getline(f, line)) {
        vector<char> row;
        for (char c : line) {
            row.push_back(c);
        }
        this->maze.push_back(row);
    }

    // Find the start position and avocado positions
    for(int row = 0; row < this->maze.size(); ++row) {
        for(int col = 0; col < this->maze[0].size(); ++col) {

            if(this->maze[row][col] == 'x') {
                this->robotRow = row;
                this->robotCol = col;
            }
            if(maze[row][col] == '@') {
                this->avocadoPositions.push_back({row, col});
            }
        }
    }
    
    // TODO delete
    for (auto avo : this->avocadoPositions){
        cout << avo.first << "," << avo.second;
        cout << "\r\n";
    }
}

/**
 * @brief Breadth-first search algorithm, which is guaranteed to find the shortest 
 * path between arbitrary start and destination points in an unweighted graph
*/
vector<vector<int>> DPGridTraversal::bfs(int startRow, int startCol) {

    // BFS depth map with same dimensions as maze, initialized to all -1s
    vector<vector<int>> bfsDepth (this->maze.size(), vector<int>(maze[0].size(), -1));

    queue<tuple<int, int, int>> bfsQueue;
    set<pair<int, int>> visitedNodes;
    
    bfsQueue.push({startRow, startCol, 0});
    visitedNodes.insert({startRow, startCol});

    while(!bfsQueue.empty()) {
        int row, col, steps;
        tie(row, col, steps) = bfsQueue.front();
        bfsQueue.pop();
        
        if(bfsDepth[row][col] == -1) {
            bfsDepth[row][col] = steps;
        }

        vector<pair<int, int>> traversalDirections{{-1, 0}, {0, -1}, {1, 0}, {0, 1}};

        for(pair<int, int> dir : traversalDirections) {
            int newRow = row + dir.first, newCol = col + dir.second;
            
            if( 0 <= newRow && 
                newRow < maze.size() && 
                0 <= newCol && 
                newCol < maze[0].size() &&
                visitedNodes.find({newRow, newCol}) == visitedNodes.end() && 
                maze[newRow][newCol] != '#') {

                bfsQueue.push({newRow, newCol, steps + 1});
                visitedNodes.insert({newRow, newCol});
            }
        }
    }

    return bfsDepth;
}

void DPGridTraversal::buildDistanceMatrix() {

    


}