from dask.distributed import Client
from queue import Queue, Empty
from time import sleep
from random import uniform


def task1(data):
    print("computing", str(data))
    sleep(uniform(0.5, 1.5))  # simulate work
    return {"x": data["x"] + 4}, "task2"


def task2(data):
    print("computing", str(data))
    sleep(uniform(0.5, 1.5))  # simulate work
    return {"x": data["x"] - 1}, "task1"


class Manager:
    def __init__(self, task_map):
        self.task_map = task_map
        self.tasks = Queue()

    def main_loop(self):
        while True:
            try:
                Task, data = self.tasks.get()
            except Empty:
                print("Queue is empty")
                continue

            print(f"submitting {Task} with {data}")
            future = client.submit(Task, data)
            future.add_done_callback(lambda future: self.done_callback(future.result()))

    def done_callback(self, result):
        print(result)
        data, *tasks = result
        for task in tasks:
            Task = self.task_map[task]
            self.tasks.put((Task, data))


if __name__ == "__main__":
    client = Client()

    manager = Manager({"task1": task1, "task2": task2})
    manager.tasks.put((task1, {"x": 1}))
    manager.main_loop()

    # result_collector()
