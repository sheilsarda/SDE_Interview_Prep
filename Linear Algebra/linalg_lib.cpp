#define PRINT_RESULT 1

#include<vector>
#include <iostream>
#include <iomanip>

using namespace std;

class Matrix {
  public:
    int n_rows;
    int n_cols;
    int **m;
    
    Matrix(int r, int c) : n_rows(r), n_cols(c) {
   
      m = (int **) malloc(n_rows * sizeof(int *));

      for(int i = 0; i < n_rows; ++i){
        m[i] = (int *) malloc(n_cols * sizeof(int));

	for(int j = 0; j < n_cols; ++j)
	  m[i][j] = 0;
      }
    }

    void print() {
      cout << "M: " << endl;
      for(int i = 0; i < n_rows; ++i){
        for(int j = 0; j < n_cols; ++j)
	  cout << setw(3) << m[i][j] << " ";
	cout << endl;
      }
      
    }
};

class MatrixOps {
  public:
  
    Matrix transpose(Matrix a){
      
      Matrix res = Matrix(a.n_cols, a.n_rows);

      for(int i = 0; i < a.n_rows; ++i)
	for(int j = 0; j < a.n_cols; ++j)
	  res.m[j][i] = a.m[i][j];

      return res;
      
    }

    Matrix multiply(Matrix m, Matrix n){
    
      return n;
    }	    
};

int main() {
 
  MatrixOps ops;

  /**
   * Test 1: Symmetric Matrix:
   * transpose should be the same as original
   */

  Matrix m1(2, 2);
  
  m1.m[0][0] = 1;
  m1.m[0][1] = 2;
  m1.m[1][0] = 2;
  m1.m[1][1] = 1;

  Matrix m3 = ops.transpose(m1);

  cout << "Test 1: Symmetric Matrix" << endl;
  m1.print();
  m3.print();


  /**
   * Test 2: Asymmetric Matrix:
   * transpose should not be the same as original
   */

  m1.m[0][0] = 1;
  m1.m[0][1] = 2;
  m1.m[1][0] = 3;
  m1.m[1][1] = 4;

  m3 = ops.transpose(m1);
  
  cout << "Test 2: Asymmetric Matrix" << endl;
  m1.print();
  m3.print();
  
  /**
   * Test 3: Rectangular Matrix:
   * transpose should not be the same as original
   */

  Matrix m2(3, 5);

  int val = 1;
  for(int i = 0; i < m2.n_rows; ++i)
    for(int j = 0; j < m2.n_cols; ++j)
      m2.m[i][j] = val++;

  m3 = ops.transpose(m2);
  
  cout << "Test 3: Rectangular Matrix" << endl;
  m2.print();
  m3.print();



  return 0;
}

