#include<vector>
#include <iostream>
#include <stdlib.h>
#include <iomanip>

using namespace std;

#define KERNEL_LEN 3
#define PRINT_RESULT 1

int main() {

  int n_rows, n_cols;

  cout << "Number of Rows: ";
  cin >> n_rows;
  cout << "Number of Cols: ";
  cin >> n_cols;

#ifdef PRINT_RESULT
  
  cout << "Entered Dimensions: (" << n_rows;
  cout << " x " << n_cols << ")" << endl;

#endif

  uint8_t M[n_rows][n_cols];
  
  int Dx[n_rows][n_cols];
  int Dy[n_rows][n_cols];  
  
  int K[3] = {-1, 0, 1};


  for(int i = 0; i < n_rows; ++i)
    for(int j = 0; j < n_cols; ++j){
      M [i][j] = rand();
      Dx[i][j] = 0;
      Dy[i][j] = 0;

    }

#ifdef PRINT_RESULT

  cout << "M: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(3) << unsigned(M[i][j]) << ' ';
    }
    cout << endl;
  }

#endif


  /**
   * For cells that are on the border
   * of matrix M (i.e. first and last
   * row / col), we apply a partial
   * convolution.
   */

  for(int i = 0; i < n_rows; ++i) 
    for(int j = 0; j < n_cols; ++j){ 
      if(j > 0 && j < n_cols - 1){
        Dy[i][j] += M[i][j-1] * K[0];
        Dy[i][j] += M[i][j  ] * K[1];
        Dy[i][j] += M[i][j+1] * K[2];
      } else if (j == 0){
        Dy[i][j] += M[i][j  ] * K[1];
        Dy[i][j] += M[i][j+1] * K[2];
      } else if (j == n_cols - 1){
        Dy[i][j] += M[i][j-1] * K[0];
        Dy[i][j] += M[i][j  ] * K[1];
      }
    }
  
 
  for(int i = 0; i < n_rows; ++i) 
    for(int j = 0; j < n_cols; ++j){
      if(i > 0 && i < n_rows - 1){
        Dx[i][j] += M[i-1][j] * K[0];
        Dx[i][j] += M[i  ][j] * K[1];
        Dx[i][j] += M[i+1][j] * K[2];
      } else if (i == 0){
        Dx[i][j] += M[i  ][j] * K[1];
        Dx[i][j] += M[i+1][j] * K[2];
      } else if (i == n_rows - 1){
        Dx[i][j] += M[i-1][j] * K[0];
        Dx[i][j] += M[i  ][j] * K[1];
      }
    }
  

#ifdef PRINT_RESULT

  cout << "Dy: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(4) << Dy[i][j] << ' ';
    }
    cout << endl;
  }

  cout << "Dx: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(4) << Dx[i][j] << ' ';
    }
    cout << endl;
  }

#endif

  return 0;
}

