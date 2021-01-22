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
      
      Matrix res = Matrix(m.n_rows, n.n_cols);

      // Return empty matrix if invalid calculation
      if(m.n_cols != n.n_rows) return Matrix(0, 0);

      for(int i = 0; i < m.n_rows; ++i)
	for(int j = 0; j < n.n_cols; ++j)      
          for(int k = 0; k < m.n_cols; ++k)
            res.m[i][j] += m.m[i][k] * n.m[k][j];

      return res;
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
  m1.m[0][1] = 0;
  m1.m[1][0] = 0;
  m1.m[1][1] = 1;

  Matrix m3 = ops.transpose(m1);

  cout << "Transpose Test 1: Symmetric Matrix" << endl;
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
  
  cout << "Transpose Test 2: Asymmetric Matrix" << endl;
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
  
  cout << "Transpose Test 3: Rectangular Matrix" << endl;
  m2.print();
  m3.print();

  /**
   * Test 4: Identity Matrix:
   * Matrix multiplied by itself should be the same
   */
  
  m1.m[0][0] = 1;
  m1.m[0][1] = 0;
  m1.m[1][0] = 0;
  m1.m[1][1] = 1;

  m3 = ops.multiply(m1, m1);

  cout << "Multiply Test 1: Identity Matrix" << endl;
  m1.print();
  m3.print();

  /**
   * Test 5: Rectangular Matrix:
   * matrix multiplied by its transpose should be 
   * symmetric
   */

  m3 = ops.transpose(m2);

  Matrix m4 = ops.multiply(m2, m3);

  cout << "Multiply Test 2: Rectangular Matrix" << endl;
  m2.print();
  m3.print();
  m4.print();

  return 0;
}

