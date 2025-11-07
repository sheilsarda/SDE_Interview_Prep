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
        std::vector<char> operator_list = {'+', '-', '*', '/', '(', ')'};
        for(int i = 0; i < s.length(); i++) {
            if (std::find(operator_list.begin(), operator_list.end(), s[i]) != operator_list.end()){
                if (last_num.length() > 0)
                    delimited_string.push_back(last_num);
                delimited_string.push_back(std::string(1, s[i]));
                last_num = "";
            } else if (isdigit(s[i])) {
                last_num += s[i];
            }
        }
        delimited_string.push_back(last_num);
        auto num_parentheses = 0;
        std::stack<string> parentheses_stack;
        for(int i = 0; i < delimited_string.size(); i++) {
            if (delimited_string[i] == "(") {
                parentheses_stack.push(delimited_string[i]);
                num_parentheses++;
            } else if (delimited_string[i] == ")") {
                num_parentheses--;
                std::vector<string> problem_within_parentheses = {};
                while(parentheses_stack.top() != "(") {
                    problem_within_parentheses.push_back(parentheses_stack.top());
                    parentheses_stack.pop();
                }
                parentheses_stack.pop();
                std::reverse(problem_within_parentheses.begin(), problem_within_parentheses.end());
                auto result = SolveNoParenthesesMathProblem(problem_within_parentheses);
                parentheses_stack.push(std::to_string(result));
            } else {
                parentheses_stack.push(delimited_string[i]);
            }
        }

        std::vector<string> final_problem = {};
        while(!parentheses_stack.empty()) {
            final_problem.push_back(parentheses_stack.top());
            parentheses_stack.pop();
        }
        std::reverse(final_problem.begin(), final_problem.end());
        return SolveNoParenthesesMathProblem(final_problem);
    }

    int SolveNoParenthesesMathProblem(std::vector<string> problem){
        std::stack<int> math_stack;
        for(int i = 0; i < problem.size(); i++) {
            if (problem[i] == "*") {
                auto int_result = math_stack.top() * stringToInteger(problem[i + 1]);
                math_stack.pop();
                math_stack.push(int_result);
                ++i;
            } else if (problem[i] == "/") {
                auto int_result = math_stack.top() / stringToInteger(problem[i + 1]);
                math_stack.pop();
                math_stack.push(int_result);
                ++i;
            } else if (problem[i] == "+") {
                math_stack.push(stringToInteger(problem[i + 1]));
                ++i;
            } else if (problem[i] == "-") {
                math_stack.push(-1 * stringToInteger(problem[i + 1]));
                ++i;
            } else if (problem[i].length() > 0) {
                math_stack.push(stringToInteger(problem[i]));
            }
        }

        int to_return = 0;
        while(!math_stack.empty()) {
            to_return += math_stack.top();
            math_stack.pop();
        }
        return to_return;
    }

    int stringToInteger(string s) {
        try{
            return stoi(s);
        } catch(const std::invalid_argument& e) {
            std::cout << "s: " << s << std::endl;
            std::cout << "Error: " << e.what() << std::endl;
            return INT_MAX;
        }
    }
};