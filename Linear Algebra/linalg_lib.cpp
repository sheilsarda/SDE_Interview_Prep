#define PRINT_RESULT 1

#include<vector>
#include <iostream>

using namespace std;

class Matrix {
  public:
    int n_rows;
    int n_cols;
    vector<vector<int>> m;
    
    Matrix(int r, int c) :
      n_rows(r), n_cols(c) {
   
      for(int i = 0; i < n_rows; ++i)
	m.push_back()
    }
};

class Computation {
  public:
    vector<float> A = { 1.5, 0.5, 0.5 , 1.5 };
  
    Point a_row1 = Point(1.5, 0.5);
    Point a_row2 = Point(0.5, 1.5);
  
    vector<Point> findPoints(vector<Point> candidates){
      
      vector<Point> toReturn;

      for (Point c :  candidates){
          Point product(c.x * a_row1.x + c.y * a_row2.x, c.x * a_row1.y + c.y * a_row2.y);
          float normL2 = product.x * product.x + product.y * product.y;
          if(normL2 < 1) toReturn.push_back(c);
        }

        return toReturn;
      
    }
};

// To execute C++, please define "int main()"
int main() {
  
  Computation c;
  
  vector<Point> candidates;
  
  /** 
   * Cases to test: 
   * L2 Norm < 1
   * L2 Norm > 1
   * L2 Norm = 1
   */

  candidates = {Point(0,0), Point(0,1)};
  vector<Point> result = c.findPoints(candidates);
  
  cout << "Size of Result: " << result.size() << endl;
  for (Point r : result)
    cout << r.x << ", " << r.y << endl;
    
  return 0;
}

