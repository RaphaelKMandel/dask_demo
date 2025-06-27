from time import sleep
from random import choice
from multiprocessing import Pool
from numpy import random
from numba import njit

@njit
def iterate(x):
    Ny, Nx = x.shape
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            x[j,i] = 0.25 * (x[j,i-1] + x[j,i+1] + x[j-1, i] + x[j+1, i])

    return x


class Physics:
    def __init__(self):
        self.array = random.random(size=(1000, 2000))

    def solve(self):
        print("solving with", str(self.array)[:10])
        for i in range(10):
            self.array = iterate(self.array)

        return self.array

    def callback(self, result):
        print("callback with ", str(result)[:10])
        self.array = result


if __name__ == "__main__":
    physics = [Physics() for i in [1, 10, 100, 1000]]
    pool = Pool(processes=4)
    for i in range(100):
        results = []
        for p in physics:
            result = pool.apply_async(p.solve, callback=p.callback)
            results.append(result)
            # result = pool.apply(worker_task, args=(i,))
            # when_done(result)
            # sleep(0.1)

        for r in results:
            r.get()

        print("\n\nNext Iteration\n\n")

    while True:
        pass

    # Optional: do other things here while task is running
    # pool.close()  # No more tasks will be submitted
    # pool.join()   # Wait for all tasks to finish
