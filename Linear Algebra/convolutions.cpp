#include<vector>
#include <iostream>
#include <stdlib.h>
#include <iomanip>

using namespace std;

#define KERNEL_LEN 3

int main() {

  int n_rows, n_cols;

  cout << "Number of Rows: ";
  cin >> n_rows;
  cout << "Number of Cols: ";
  cin >> n_cols;

  cout << "Entered Dimensions: (" << n_rows;
  cout << " x " << n_cols << ")" << endl;

  uint8_t M[n_rows][n_cols];
  
  int Dx[n_rows][n_cols];
  int Dy[n_rows][n_cols];  
  
  int K[3] = {-1, 0, 1};
  
  /**
   * You are free to decide how you want to 
   * deal with border conditions. Just 
   * explicitly state your assumption 
   * in a comment in the solution.
   */
   
  cout << "M: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(3) << unsigned(M[i][j]) << ' ';
    }
    cout << endl;
  }

  for(int i = 0; i < n_rows; ++i) 
    for(int j = 0; j < n_cols; ++j) 
      if(j > 0 && j < n_cols - 1){
        Dy[i][j] += M[i][j-1] * K[0];
        Dy[i][j] += M[i][j  ] * K[1];
        Dy[i][j] += M[i][j+1] * K[2];
      }
  
  cout << "Dy: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(4) << Dy[i][j] << ' ';
    }
    cout << endl;
  }
 
  for(int i = 0; i < n_rows; ++i) 
    for(int j = 0; j < n_cols; ++j) 
      if(i > 0 && i < n_rows - 1){
        Dx[i][j] += M[i-1][j] * K[0];
        Dx[i][j] += M[i  ][j] * K[1];
        Dx[i][j] += M[i+1][j] * K[2];
      }
  
   
  cout << "Dx: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(4) << Dx[i][j] << ' ';
    }
    cout << endl;
  }
      
  return 0;
}
