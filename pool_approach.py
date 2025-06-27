from time import sleep
from random import choice
from multiprocessing import Pool

def worker_task(x):
    print("worker", x)
    sleep(choice([0.1 * i for i in range(10)]))
    return "this", "that", x * x

def when_done(result):
    print(f"Result received: {result}")

if __name__ == "__main__":
        pool = Pool(processes=4)
        for i in range(10):
            pool.apply_async(worker_task, args=(i,), callback=when_done)
            # result = pool.apply(worker_task, args=(i,))
            # when_done(result)
            sleep(0.1)

        while True:
            pass

        # Optional: do other things here while task is running
        # pool.close()  # No more tasks will be submitted
        # pool.join()   # Wait for all tasks to finish
