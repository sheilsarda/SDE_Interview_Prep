#include <vector>
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

        std::cout << "delimited_string: ";
        for(auto &str : delimited_string){
            std::cout << str << "|";
        }
        std::cout << std::endl;
        std::vector<std::vector<char>> operator_list = { {'*', '/'}, {'+', '-'} };
        auto operator_idx = 0;


        while(operator_idx != operator_list.size()){          
            auto equal_precedence_operators = operator_list[operator_idx]; 
            std::cout << "equal_precedence_operators: ";
            for(auto &op : equal_precedence_operators){
                std::cout << op << "|";
            }
            std::cout << std::endl;
            auto equal_precedence_operator_itr = std::for_each(equal_precedence_operators.begin(), equal_precedence_operators.end(), [&](char op){
                return std::find(
                    delimited_string.begin(), 
                    delimited_string.end(), 
                    std::string(1, op));
            });
            auto operator_itr = std::min_element(equal_precedence_operator_itr.begin(), equal_precedence_operator_itr.end());
            std::cout << "operator_itr: " << operator_itr << std::endl;

            std::string result = "";
            auto int_result = 0;
            switch (operator_itr){
                case '*': 
                    int_result = stoi(delimited_string[operator_itr - 1]) * stoi(delimited_string[operator_itr + 1]);    
                    result = std::to_string(int_result);
                    break;
                case '/':
                    int_result = stoi(delimited_string[operator_itr - 1]) / stoi(delimited_string[operator_itr + 1]);    
                    result = std::to_string(int_result);
                    break;
                case '+':
                    int_result = stoi(delimited_string[operator_itr - 1]) + stoi(delimited_string[operator_itr + 1]);    
                    result = std::to_string(int_result);
                    break;
                case '-':
                    int_result = stoi(delimited_string[operator_itr - 1]) - stoi(delimited_string[operator_itr + 1]);    
                    result = std::to_string(int_result);
                    break;                    
            }
            
            // Build a new vector with the result replacing the operand-operator-operand sequence
            std::vector<string> new_problem(delimited_string.begin(), delimited_string.begin() + operator_itr - 1);
            new_problem.push_back(result);
            new_problem.insert(new_problem.end(), delimited_string.begin() + operator_itr + 2, delimited_string.end());
            std::cout << "new_problem: ";
            for(auto &str : new_problem){
                std::cout << str << "|";
            }
            std::cout << std::endl;
            
            // Replace the current delimited_string with the new one and continue
            delimited_string = new_problem;
        }
        return stoi(delimited_string[0]);
    }
};