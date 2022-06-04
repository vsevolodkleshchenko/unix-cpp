#include <iostream>
#include <ctime>
#include <thread>
#include <omp.h>
using namespace std;


int func1(int &x, int num_of_it)
{
	for (int i = 0; i < num_of_it - 1; i++) 
	{
		x * x - x * x + x * 4 - x * 5 + x + x;
	}
	x = x * x - x * x + x * 4 - x * 5 + x + x;
	return x;
}


int func2(int &x, int num_of_it)
{
	for (int i = 0; i < num_of_it - 1; i++)
	{
		x + x;
	}
	x = x + x;
	return x;
}


int func3(int &x, int num_of_it)
{
	int f1 = func1(x, num_of_it);
	int f2 = func2(x, num_of_it);
	x = f1 + f2 - f1;
	return x;
}


/* int thrfunc3(int x, int num_of_it)
{
	int r1 = x;
	int r2 = x;
	thread thrfor1(func1, ref(r1), num_of_it);
	thread thrfor2(func2, ref(r2), num_of_it);
	thrfor1.join();
	thrfor2.join();
	x = r1 + r2 - r1;
	return x;
} */


void seq(int x, int num_of_it)
{
	unsigned int start_time, end_time, end_time1, end_time2;
	start_time = clock();
	func1(x, num_of_it);
	end_time1 = clock();
	func2(x, num_of_it);
	end_time2 = clock();
	func3(x, num_of_it);
	end_time = clock();
	cout << "Sequence " << num_of_it << "itrs: " << float(end_time - start_time) / CLOCKS_PER_SEC << endl;
	cout << "  Func 1: " << float(end_time1 - start_time) / CLOCKS_PER_SEC << endl;
	cout << "  Func 2: " << float(end_time2 - end_time1) / CLOCKS_PER_SEC << endl;
	cout << "  Func 3: " << float(end_time - end_time2) / CLOCKS_PER_SEC << endl;
}


void thr(int x, int num_of_itrs)
{
	unsigned int start_time, end_time, end_time1;
	int res1 = x;
	int res2 = x;
	int res3 = x;
	start_time = clock();
	thread thr1(func1, ref(res1), num_of_itrs);
	thread thr2(func2, ref(res2), num_of_itrs);
	thr1.join();
	thr2.join();
	end_time1 = clock();
	res3 = res1 + res2 - res1;
	end_time = clock();
	cout << "Threads " << num_of_itrs << "itrs: " << float(end_time - start_time) / CLOCKS_PER_SEC << endl;
	cout << "  Func 1,2: " << float(end_time1 - start_time) / CLOCKS_PER_SEC << endl;
	cout << "  Func 3: " << float(end_time - end_time1) / CLOCKS_PER_SEC << endl;
}


int main()
{
	int x = 3;
	seq(x, 1'000'000);
	x = 3;
	seq(x, 10'000'000);
	x = 3;
	thr(x, 1'000'000);
	x = 3;
	thr(x, 10'000'000);

	//unsigned int start_time, end_time;
	//start_time = clock();
	//func3(x, 10'000'000);
	//end_time = clock();
	//cout << "Time f3 10 000 000itrs: " << float(end_time - start_time) / CLOCKS_PER_SEC << endl;
}
