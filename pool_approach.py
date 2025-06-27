from time import sleep, time as tic
from random import choice
from multiprocessing import Pool
from numpy import random
from numba import njit


@njit
def iterate(x, N=3):
    Ny, Nx = x.shape
    for n in range(N):
        for j in range(1, Ny - 1):
            for i in range(1, Nx - 1):
                x[j, i] = 0.25 * (x[j, i - 1] + x[j, i + 1] + x[j - 1, i] + x[j + 1, i])

    return x


class Physics:
    def __init__(self):
        self.array = random.random(size=(1000, 1000))

    def solve(self):
        # print("solving with", str(self.array)[:10])
        self.array = iterate(self.array)

        return self.array

    def callback(self, result):
        # print("callback with ", str(result)[:10])
        self.array = result


def time_pool():
    results = []
    for p in physics:
        result = pool.apply_async(p.solve, callback=p.callback)
        results.append(result)

    # result = pool.apply(worker_task, args=(i,))
    # when_done(result)
    # sleep(0.1)

    for r in results:
        r.get()


def time_gil():
    for p in physics:
        p.solve()


def time(func):
    t0 = tic()
    func()
    print(f"Elapsed time of {func.__name__} is {(tic() - t0)} s.")


if __name__ == "__main__":
    N = 10
    physics = [Physics() for i in range(10)]
    pool = Pool(processes=N)

    for func in [time_gil, time_pool]:
        for n in range(3):
            time(func)
