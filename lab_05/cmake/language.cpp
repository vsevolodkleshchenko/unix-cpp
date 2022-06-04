#include <iostream>
#include <cstring>
#include <sstream>
#include <map>
#include <fstream>
#include <vector>
#include <thread>
#include <ctime>

using namespace std;

class operation
{
public:
    string PCONS = "PCONS";
    string PFILE = "PFILE";
    string CALC = "CALC";
    string LOOP = "LOOP";

    const int iPCONS = 1;
    const int iPFILE = 2;
    const int iCALC = 3;
    const int iLOOP = 4;

    //void cprint(string s);
    //void fprint(string s);
    //double calc(double operand1, char operator1, double operand2);
};

class consop : public operation
{
public:
    void cprint(string s);
};

class fileop: public operation
{
public:
    void fprint(string s);
};

class mathop: public operation
{
public:
    double calc(double operand1, char operator1, double operand2);
};

void consop::cprint(string s) {
    cout << s << " ";
}


void fileop::fprint(string s) {
    std::ofstream out("..\\outfile.txt", std::ios::app);
    if (out.is_open())
        out << s << " ";
    out.close();
}

double mathop::calc(double operand1, char operator1, double operand2) {
    switch (operator1) {
    case '+':
        return operand1 + operand2;
        break;
    case '-':
        return operand1 - operand2;
        break;
    case '*':
        return operand1 * operand2;
        break;
    case '/':
        return operand1 / operand2;
        break;
    default:
        break;
    }
}


void submain(string cmds)
{
    operation op;
    fileop fop;
    consop cop;
    mathop mop;
    map <string, int> mapping;
    mapping[cop.PCONS] = cop.iPCONS;
    mapping[fop.PFILE] = fop.iPFILE;
    mapping[mop.CALC] = mop.iCALC;
    mapping[op.LOOP] = op.iLOOP;
    mapping[";"] = 5;

    istringstream iss(cmds);
    string cmd;
    string sstr;
    int num2, num = 0;

    while (iss >> cmd) {
        pt:
        switch (mapping[cmd])
        {
        case 1:
            while (cmd != ";") {
                iss >> cmd;
                if (cmd == op.CALC) {
                    double operand1;
                    char operator1;
                    double operand2;
                    iss >> operand1;
                    iss >> operator1;
                    iss >> operand2;
                    cmd = to_string(mop.calc(operand1, operator1, operand2));
                }
                if (cmd != ";")
                    cop.cprint(cmd);
            }
            goto pt;
            break;
        case 2:
            while (cmd != ";") {
                iss >> cmd;
                if (cmd == op.CALC) {
                    double operand1;
                    char operator1;
                    double operand2;
                    iss >> operand1;
                    iss >> operator1;
                    iss >> operand2;
                    cmd = to_string(mop.calc(operand1, operator1, operand2));
                }
                if (cmd != ";")
                    fop.fprint(cmd);
            }
            goto pt;
            break;
        case 3:
            double operand1;
            char operator1;
            double operand2;
            iss >> operand1;
            iss >> operator1;
            iss >> operand2;
            mop.calc(operand1, operator1, operand2);
            iss >> cmd;
            goto pt;
            break;
        case 4:
            num2 = cmds.find("]", num + 5);
            sstr = cmds.substr(num + 5, num2 - num - 5);
            iss >> num2;
            for (int i = 0; i < num2 - 1; i++)
                submain(sstr);
            break;
        case 5:
            num = cmds.find(";", num + 1);
            break;
        default:
            break;
        }
    }
}

void doprog(string* prgrm, int count) {
    vector <thread> th_vec;
    vector <int> time_vec;
    for (int i = 0; i < count; i++) {
        string cmds = prgrm[i];
        th_vec.push_back(std::thread(submain, cmds));
        time_vec.push_back(clock());
    }
    for (int i = 0; i < count; i++) {
        th_vec.at(i).join();
        cout << "\n<line :" << i + 1 << ">" << ": ";
        cout << float(clock() - time_vec.at(i)) / CLOCKS_PER_SEC << "s" << endl;
    }
}


int main() {
    string* AS;
    string* AS2;
    int count;
    string s;
    char buf[80];
    cout << "Enter programm:\n";
    count = 0;
    AS = nullptr;
    do {
        cout << "=> ";
        cin.getline(buf, 80, '\n');
        s = buf;
        if (s != "")
        {
            count++;
            AS2 = new string[count];
            for (int i = 0; i < count - 1; i++)
                AS2[i] = AS[i];
            AS2[count - 1] = s;
            if (AS != nullptr)
                delete[] AS;
            AS = AS2;
        }
    } while (s != "");
    cout << "\nResults:\n";
    if (count > 0)
        doprog(AS, count);
    delete[] AS;
}
