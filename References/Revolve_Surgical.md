````cpp
// Inputs: 2 signed integers
// Output: True if both inputs have same sign; false otherwise

// Test Case 1: -1, -3: true
// Test Case 2: 2, -1: false
// Test Case 3: 0, 0: true

// Edge Case 1: unsigned int #FFFF, int 1: false
// Edge Case 2: 3, 0: false
// Edge Case 3: -3, 0: false

// 0111 1111 1111 1111 : sign bit is positive (0)
// 1111 1111 1111 1111 : sign bit is negative (1)

bool compareSigns(int input1, int input2){
	if(input1 < 0 && input2 < 0){
  	return true;
  } else if(input1 > 0 && input2 > 0){
  	return true;
  } else if(!input1 && !input2){
  	return true;
  } else {  
  	return false;
  }
}



template<input1, input2>
bool compareSigns(input1, input2){

}

#include <concepts>

template<std::integral T>
bool compareSigns(T input1, T input2);
````