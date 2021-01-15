#include<vector>
#include <iostream>
using namespace std;

class Point {
  public:
    float x;
    float y;
    
    Point(float xx, float yy) :
      x(xx), y(yy) {}
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

  int n_rows, n_cols;

  cout << "Number of Rows: ";
  cin >> n_rows;
  cout << "Number of Cols: ";
  cin >> n_cols;

  cout << "Entered Dimensions: (" << n_rows << " x " << n_cols << ")" << endl;

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
