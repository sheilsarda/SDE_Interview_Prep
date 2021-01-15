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
  
  
  for(int i = 0; i < n_rows; ++i)
    for(int j = 0; j < n_cols; ++j){
      M[i][j] = rand() % 255;
    }
   
  cout << "M: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(3) << unsigned(M[i][j]) << ' ';
    }
    cout << endl;
  }
   for(int i = 0; i < n_rows; ++i) 
    for(int j = 0; j < n_cols; ++j) 
      for(int k = 0; k < KERNEL_LEN; ++k) 
        if(j-k >= 0 && j-k < n_cols)
            Dx[i][j] += M[i][j-k] * K[k];
  
  cout << "Dx: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(5) << Dx[i][j] << ' ';
    }
    cout << endl;
  }
 
  for(int i = 0; i < n_rows; ++i) 
    for(int j = 0; j < n_cols; ++j) 
      for(int k = 0; k < KERNEL_LEN; ++k) 
        if(j-k >= 0 && j-k < n_cols)
            Dx[i][j] += M[i][j-k] * K[k];
   
   
  cout << "Dx: " << endl;
  for (int i = 0; i < n_rows; ++i){
    for (int j = 0; j < n_cols; ++j){
      cout << setw(5) << Dx[i][j] << ' ';
    }
    cout << endl;
  }
      
  return 0;
}
