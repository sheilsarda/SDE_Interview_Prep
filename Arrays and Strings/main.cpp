#include <iostream>
#include <string>
#include <map>

using namespace std;


class Solution {
private:

public:
    std::map<int, bool> openParaIdx, closeParaIdx;

    int findClosingPara(int startSearchIdx){
        if(openParaIdx[startSearchIdx]){
            int recursiveLen =0;
            recursiveLen = findClosingPara(startSearchIdx+1);
            if(recursiveLen > 0 && closeParaIdx[recursiveLen+startSearchIdx-1]) 
                return 2+recursiveLen;
            else
                return -1;
        }
        else if(closeParaIdx[startSearchIdx]){
            if(openParaIdx[startSearchIdx + 1])
                return 2+findClosingPara(startSearchIdx + 2);
            return 2;
        }
        return -1;
    }
    
    int longestValidParentheses(string s) {
        for(int strIdx=0; strIdx<s.length(); ++strIdx){
            if(s[strIdx] == '(') 
                openParaIdx[strIdx] = true;
            else if(s[strIdx] == ')')
                closeParaIdx[strIdx] = true;
            else{
                openParaIdx[strIdx] = false;
                closeParaIdx[strIdx] = false;
            }  
        }

        int longestValidPara = 0, strIdx = 0;
        while(strIdx <s.length()){
            int lenOfSubstring = 0;
            if(openParaIdx[strIdx]){
                lenOfSubstring = findClosingPara(strIdx + 1);
                longestValidPara = max(longestValidPara, lenOfSubstring);
                strIdx += max(lenOfSubstring-1,0);
            }
            else
                strIdx += 1;   
        }
        return longestValidPara;
    }
};

int main(){
    Solution sol;
    cout << sol.longestValidParentheses("(()");
    return 0;
}