#define PRINT_RESULT 1

#include<vector>
#include <iostream>

using namespace std;

class Matrix {
  public:
    int n_rows;
    int n_cols;
    int *m;
    
    Matrix(int r, int c) :
      n_rows(r), n_cols(c) {
   
      m = int[n_rows][n_cols];
      for(int i = 0; i < n_rows; ++i)
        for(int j = 0; j < n_cols; ++j)
	  m[i][j] = 0;
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
  
  return 0;
}

