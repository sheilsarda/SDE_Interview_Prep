#include <vector>
#include <stack>
#include <string>
#include <algorithm>
using namespace std;
class Solution {
public:

    int calculate(string s) {
        std::string last_num = "";
        std::vector<string> delimited_string;
        for(int i = 0; i < s.length(); i++) {
            if (s[i] == '+' || s[i] == '-' || s[i] == '*' || s[i] == '/'){
                delimited_string.push_back(last_num);
                delimited_string.push_back(std::string(1, s[i]));
                last_num = "";
            } else if (s[i] != ' ') {
                last_num += s[i];
            }
        }
        delimited_string.push_back(last_num);

        std::stack<int> math_stack;
        for(int i = 0; i < delimited_string.size(); i++) {
            if (delimited_string[i] == "*") {
                auto int_result = math_stack.top() * stoi(delimited_string[i + 1]);
                math_stack.pop();
                math_stack.push(int_result);
                ++i;
            } else if (delimited_string[i] == "/") {
                auto int_result = math_stack.top() / stoi(delimited_string[i + 1]);
                math_stack.pop();
                math_stack.push(int_result);
                ++i;
            } else if (delimited_string[i] == "+") {
                math_stack.push(stoi(delimited_string[i + 1]));
                ++i;
            } else if (delimited_string[i] == "-") {
                math_stack.push(-1 * stoi(delimited_string[i + 1]));
                ++i;
            } else {
                math_stack.push(stoi(delimited_string[i]));
            }
        }

        auto to_return = 0;
        while(!math_stack.empty()) {
            to_return += math_stack.top();
            math_stack.pop();
        }
        return to_return;
    }
};