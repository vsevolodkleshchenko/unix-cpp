#include <iostream>
using namespace std;


template <class T>
struct Elem
{
    T data;
    Elem* next;
    Elem* prev;
};


template <class T>
class List
{
    Elem<T>* begin;
    Elem<T>* end;
    int count;

public:
    List()
    {
        begin = end = nullptr;
        count = 0;
    }

    void append(T newdata)
    {
        Elem<T>* elem = new Elem<T>;
        elem->next = nullptr;
        elem->data = newdata;
        elem->prev = end;
        if (end == nullptr)
            begin = end = elem;
        else
        {
            end->next = elem;
            end = elem;
        }
        count++;
    }

    void print()
    {
        if (count != 0)
        {
            Elem<T>* curr = begin;
            cout << "[ ";
            while (curr != nullptr)
            {
                cout << curr->data << " ";
                curr = curr->next;
            }
            cout << " ]";
        }
    }

    void clear()
    {
        while (begin != nullptr)
        {
            Elem<T>* del = begin;
            begin = begin->next;
            delete del;
        }

    }

    //~List()
    //{
    //    clear();
    //}
};


List<char> hanoi(int n, char s, char f, char h, List<char> L)
{
    if (n == 0)
        return L;
    L = hanoi(n - 1, s, h, f, L);
    L.append(s);
    L.append('-');
    L.append(f);
    L.append(' ');
    L = hanoi(n - 1, h, f, s, L);
    return L;
}


int main()
{
    int n = 6;
    List<char> L;
    L = hanoi(n, 's', 'f', 'h', L);
    L.print();
    L.clear();
    L.print();
}

