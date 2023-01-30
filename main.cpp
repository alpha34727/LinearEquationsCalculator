#include <iostream>
#include <sstream>

using namespace std;

int main()
{
    string str;
    double a1, b1, c1, a2, b2, c2;

    cin >> str;

    for (int i = 0; i < str.size(); i++){
        cout << str[i] << " ";
        if (str[i] == '+' || str[i] == '-'){
            str.insert(i, " ");
        }
    }

    cout << str;


    return 0;
}
