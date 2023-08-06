from time import sleep
from parfor import parfor


def my_fun(*args, **kwargs):
    @parfor(range(10), (3,))
    def fun(i, a):
        sleep(1)
        return a * i ** 2

    return fun


if __name__ == '__main__':
    print(my_fun())