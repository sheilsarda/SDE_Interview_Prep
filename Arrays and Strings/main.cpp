#include <iostream>
#include <string>
#include <map>
using namespace std;

class Solution {
public:
    int longestValidParentheses(string s) {
        int left=0;
        int right=0;
        int ans=0;
        int n=s.size();
        for(int i=0;i<n;i++){
            if(s[i]=='(')left++;
            else right++;
            if(left==right)ans=max(ans,right*2);
            else if(right>left)left=right=0;
        }
        left=right=0;
        for(int i=n-1;i>=0;i--){
            if(s[i]==')')right++;
            else left++;
            if(left==right)ans=max(ans,right*2);
            else if(left>right)left=right=0;
        }
        return ans;
    }
};

int main(){
    Solution sol;
    cout << sol.longestValidParentheses("()(())");
    return 0;
}