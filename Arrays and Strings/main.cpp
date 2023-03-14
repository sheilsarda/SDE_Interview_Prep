#include <iostream>
#include <string>
#include <map>
using namespace std;

class Solution {
private:

public:
    std::map<int, bool> openParaIdx, closeParaIdx;
    string s;

    int findClosingPara(int startSearchIdx){
        if(openParaIdx[startSearchIdx]){
            int recursiveLen =0;
            recursiveLen = findClosingPara(startSearchIdx+1);
            if(recursiveLen > 0){
                if(recursiveLen + startSearchIdx + 2 < s.length() && 
                    closeParaIdx[recursiveLen+startSearchIdx]) 
                    return 2+recursiveLen;
                else 
                    return recursiveLen;
            }
            else
                return -1;
        }
        else if(closeParaIdx[startSearchIdx]){
            if(startSearchIdx+1<s.length() && openParaIdx[startSearchIdx + 1]){
                return 2+findClosingPara(startSearchIdx + 2);
                
            } else
                return 2;
        }
        return -1;
    }
    
    int longestValidParentheses(string s) {
        this->s = s;
        if(s.length() < 2) 
            return 0;
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

        int longestValidPara = 0, endIdx = 0, strIdx = 0;
        while(strIdx <s.length()){
            int lenOfSubstring = 0;
            if(openParaIdx[strIdx]){
                if(strIdx + 1 < s.length())
                    lenOfSubstring = findClosingPara(strIdx + 1);
                else
                    return 0;
                
                if(endIdx + 1 == strIdx)
                    longestValidPara += lenOfSubstring;
                else
                    longestValidPara = max(longestValidPara, lenOfSubstring);
                
                endIdx = strIdx + lenOfSubstring;
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
    cout << sol.longestValidParentheses("()(())");
    return 0;
}