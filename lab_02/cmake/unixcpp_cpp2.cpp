#include <iostream>
#include <cmath>
#include <ctime>

using namespace std;


void f(int x)
{
    pow(x, 2) - pow(x, 2) + x * 4 - x * 5 + x + x;
}


int main()
{
    int n;
    unsigned int start_time, end_time, d_time;
    
    while (cin >> n)
    {
        cout << n << endl;
        start_time = clock();

        for (int i = 1; i <= n; i++)
        {
            f(n);
        }

        end_time = clock();
        d_time = end_time - start_time;
        cout << d_time << endl;
    }
}
