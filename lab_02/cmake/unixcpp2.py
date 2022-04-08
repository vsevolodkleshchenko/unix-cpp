import time


def f(x):
    return x ** 2 - x ** 2 + x * 4 - x * 5 + x + x


def main():
    n = input()
    while (not n.isalpha()):
        n = int(float(n))
        start_time = time.process_time()
        for i in range(n):
            f(n)
        end_time = time.process_time()
        t = end_time - start_time
        print(int(t*1000))
        n = input()


main()
