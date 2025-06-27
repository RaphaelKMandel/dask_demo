from time import sleep
from random import choice
from multiprocessing import Pool
from numpy import random


class Physics:
    def __init__(self, x):
        self.x = x
        self.array = x * random.random(size=(1000, 1000))

    def solve(self):
        print("solving with", str(self.x)[:10])
        for i in range(100):
            self.x += self.array.sum() / 1e6
            self.array -= self.x

        return self.array + self.x

    def callback(self, result):
        print("callback with ", str(result)[:10])
        self.x = result


if __name__ == "__main__":
    physics = [Physics(i) for i in [1, 10, 100, 1000]]
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
