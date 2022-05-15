// calc.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>

double pow(double operand1, double operand2)
{
    double result = 1.0;
    for (int i = 1; i <= operand2; i++)
        result *= operand1;
    return result;
}

double calculator(double operand1, char operator1, double operand2)
{
    switch (operator1)
    {
        case '+':
            return operand1 + operand2;
        case '-':
            return operand1 - operand2;
        case '^':
            return pow(operand1, operand2);
        default:
            break;
    }
}


int main()
{
    int operand1, operand2;
    char operator1;

    std::cout << "Format: a+b | a-b | a^b" << std::endl;
    std::cin >> operand1 >> operator1 >> operand2;
    std::cout << calculator(operand1, operator1, operand2);
}

