#include "DPSoln.h"
using namespace std;

struct hashPair {
    template <class T1, class T2>
    size_t operator()(const pair<T1, T2>& p) const
    {
        auto hash1 = hash<T1>{}(p.first);
        auto hash2 = hash<T2>{}(p.second);
 
        if (hash1 != hash2) {
            return hash1 ^ hash2;             
        }
         
        // If hash1 == hash2, their XOR is zero.
          return hash1;
    }
};


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
    // for (auto avo : this->avocadoPositions){
    //     cout << avo.first << "," << avo.second;
    //     cout << "\r\n";
    // }
    this->buildDistanceMatrix();
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
    /* 
     * Distance matrix = [n + 1][n +1] where n = number of avocados
     * 0th index on row and column axis represents start position of robot
     * ith index where i>0 represents the avocado at index i of avocado_positions array
     *
     * Value at distanceMat[i][j] = distanceMat[j][i] = shortest path length between ith 
     * and jth avocado (where start position counts as avocado as well) 
     */

    this->distanceMat = vector<vector<int>>(this->avocadoPositions.size() + 1, 
                                             vector<int>(this->avocadoPositions.size() + 1, 0));

    for(int i = 0; i < this->distanceMat.size(); ++i) {
        int startRow, startCol;
        if(i == 0) {
            startRow = this->robotRow;
            startCol = this->robotCol;
        } else {
            startRow = this->avocadoPositions[i - 1].first;
            startCol = this->avocadoPositions[i - 1].second;
        }

        vector<vector<int>> bfsDepth = this->bfs(startRow, startCol);

        for(int avoIdx = 0; avoIdx < this->avocadoPositions.size(); ++avoIdx) {
            if(i == avoIdx + 1) continue;

            pair<int, int> avocadoPos = this->avocadoPositions[avoIdx];

            this->distanceMat[avoIdx + 1][i] = bfsDepth[avocadoPos.first][avocadoPos.second];
            this->distanceMat[i][avoIdx + 1] = bfsDepth[avocadoPos.first][avocadoPos.second];
        }
    }

    return;
}

void generate_combinations(vector<int>& nums, int k, vector<int>& current, int start, vector<vector<int>>& result) {
    if (current.size() == k) { // Base case: current combination has k elements
        result.push_back(current);
        return;
    }
    for (int i = start; i < nums.size(); i++) {
        current.push_back(nums[i]); // Add current element to current combination
        generate_combinations(nums, k, current, i + 1, result); // Recursive call for next element
        current.pop_back(); // Backtrack and remove last element
    }
}

vector<vector<int>> DPGridTraversal::combinations(vector<int> nums, int k) {

    vector<vector<int>> result;
    vector<int> current;
    generate_combinations(nums, k, current, 0, result); // Start with first element
    
    // TODO delete
    // cout << result.size() << " size of results\r\n";
    
    return result;
}


bool DPGridTraversal::comparePairs(const pair<int, int>& p1, const pair<int, int>& p2) {
    return p1.first < p2.first;
}


pair<int, vector<pair<int, int>>> DPGridTraversal::findOptimalPath() {
    
    int pathSize = this->distanceMat.size();
    
    vector<int> rangeArray(pathSize - 1); // holds [1, 2, 3, ..., pathSize - 1]
    iota(rangeArray.begin(), rangeArray.end(), 1); // populates array     

    /**
     * Hashmap to map each subset of the nodes to a corresponding cost to reach that subset from the start node;
     * Also tracks which node it passed before reaching this subset. Node subsets are represented as set bits.
     * Key of costmap is a pair: (binary representation of set of nodes in subset, index of node)
     * Value of costmap is a pair: (distance from start, node passed to get there)
    */
    unordered_map<pair<int, int>, pair<int, int>, hashPair> costMap;
    
    for (int i = 1; i < pathSize; i++) {
        costMap[{1 << i, i}] = {this->distanceMat[0][i], 0};
    }

    // TODO delete
    // int numSubsets = 0;

    // Iterate subsets of increasing length and store intermediate results
    for (int subsetSize = 2; subsetSize < pathSize; subsetSize++) {

        // Generates subset_size subsets from the list [1, 2, 3..., path_size-1]
        for (auto subset : combinations(rangeArray, subsetSize)) {

            // TODO delete
            // numSubsets++;
            // for (auto entry : subset) cout << entry << ", ";
            // cout << "\r\n";
            
            int bits = 0;
            for (int bit: subset) {
                bits |= 1 << bit;
            }        

            // TODO rename k and m to something more descriptive
            for (int k: subset) {
                int prev = bits & ~(1 << k);
                vector<pair<int, int>> res;
            
                for (int m: subset) {
                    if (m == 0 || m == k) {
                        continue; // Symbolizes start location or the current node itself
                    }
                    res.push_back({costMap[{prev, m}].first + this->distanceMat[m][k], m});
                }
            
                costMap[{bits, k}] = *min_element(res.begin(), res.end(), this->comparePairs);
            }
        }
    }

    // TODO delete
    // cout << costMap.size() << " entries in costMap\r\n";
    // cout << numSubsets << " subsets evaluated\r\n";
    // for (const auto& [key, value] : costMap) {
    //     std::cout << "{" << key.first << ", " << key.second << "}: {" << value.first << ", " << value.second << "}\n";
    // }

    int bits = (1 << pathSize) - 2;
    
    // TODO delete
    cout << "bits: " << bitset<8>(bits) << endl;

    vector<pair<int, int>> res;
    for (int k = 1; k < pathSize; k++) {
        res.push_back({costMap[{bits, k}].first, k});
    }

    auto it = min_element(res.begin(), res.end(), this->comparePairs);
    
    int minPathLen = it->first, parent = it->second;
    
    vector<int> path;
    for (int i = 0; i < pathSize - 1; i++) {

        path.push_back(parent);
        int new_bits = bits & ~(1 << parent);        
        parent = costMap[{bits, parent}].second;
        bits = new_bits;
    }

    reverse(path.begin(), path.end());

    vector<pair<int, int>> pathCoords;
    
    for (auto avocadoIdx: path) {
        auto pos = avocadoPositions[avocadoIdx-1];
        pathCoords.push_back(pos);
    }

    ofstream file;
    file.open(this->outputFileName);
    file << minPathLen << '\n';
    for (auto coord: pathCoords) {
        file << coord.first << ',' << coord.second << '\n';
    }
    file.close();

    return make_pair(minPathLen, pathCoords);
}
