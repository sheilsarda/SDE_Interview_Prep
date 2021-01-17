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
   
      m = (int **) malloc(n_rows * n_cols * sizeof(int));

      for(int i = 0; i < n_rows; ++i)
        for(int j = 0; j < n_cols; ++j)
	  m[i][j] = 0;

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
  
    Matrix transpose(Matrix m){
      
        return m;
      
    }

    Matrix multiply(Matrix m, Matrix n){
    
      return n;
    }	    
};

int main() {
 
  MatrixOps ops;
  Matrix m1(2, 2);
  m1.m[0][0] = 1;
  m1.m[1][1] = 1;
/*

  Matrix m3 = ops.transpose(m1);
  m3.print();

  Matrix m2(2, 2);

*/
  return 0;
}

