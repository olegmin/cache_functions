# Вспомогательная часть, менять нельзя:
import time


class Timer(object):
    def __init__(self, name=None):
        self.name = name
        self.tstart = time.time()

    def __enter__(self):
        self.tstart = time.time()
        return self

    def elapsed_s(self):
        return time.time() - self.tstart

    def __exit__(self, type, value, traceback):
        if self.name:
            print(f'{self.name}')
        v = self.elapsed_s()
        if v > 1:
            print(f'Elapsed: {self.elapsed_s():0.2f} s')
        elif v > 0.001:
            print(f'Elapsed: {self.elapsed_s():0.4f} s')
        else:
            print(f'Elapsed: {self.elapsed_s():0.9f} s')

    def __repr__(self):
        return f'Timer(tstart={self.tstart}, elapsed={self.elapsed_s():0.5f}'


def slowly_process(s):
    # s = s * 0.01 # для временного ускорения запуска без кэша
    time.sleep(s)
    print(f"slowly processed for {s} s")


storage = {}


def cache(func):
    def wrapped(*args, **kwargs):
        func_name = func.__name__
        if func_name not in storage:
            storage[func_name] = dict()

        arguments = list()
        for arg in args:
            arguments.append(arg)
        for _, v in kwargs.items():
            arguments.append(v)
        arguments = tuple(arguments)

        if arguments not in storage[func_name]:
            storage[func_name][arguments] = func(*arguments)

        return storage[func_name][arguments]

    return wrapped


# Код функций - внутри функций код менять нельзя,
# но к функциям можно добавить атрибуты через @:
@cache
def f1(a):
    slowly_process(1)
    return a + 0.1


@cache
def f2(a, b):
    slowly_process(1)
    return f1(a)*2 + b


@cache
def f3(a, b, c):
    slowly_process(1)
    return f2(a, b) + c


# Код запуска “расчета”, его менять тоже нельзя:
with Timer():
    for i in range(10):
        print(f"f1({i})={f1(i)}")

    for i in range(5):
        for j in range(5):
            print(f"f2({i},{j})={f2(i,j)}")

    for i in range(3):
        for j in range(2):
            print(f"f3({i},{j}, c=-100)={f3(i,j, c=-100)}")
