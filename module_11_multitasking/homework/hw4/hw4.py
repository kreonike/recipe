import queue
import random
import threading
import time
from typing import Callable, Any


class Task:
    def __init__(self, priority: int, func: Callable, *args: Any, **kwargs: Any):
        self.priority = priority
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        self.func(*self.args, **self.kwargs)

    def __repr__(self):
        return f'Task(priority={self.priority})'

    def __lt__(self, other):
        return self.priority < other.priority


class Producer(threading.Thread):
    def __init__(self, task_queue: queue.PriorityQueue, num_tasks: int):
        super().__init__()
        self.task_queue = task_queue
        self.num_tasks = num_tasks

    def run(self):
        print('Producer: Running')
        for _ in range(self.num_tasks):
            priority = random.randint(0, 10)
            sleep_time = random.random()
            task = Task(priority, time.sleep, sleep_time)
            self.task_queue.put((priority, task))
            print(f'>added {task}.      sleep({sleep_time})')
        print('Producer: Done')


class Consumer(threading.Thread):
    def __init__(self, task_queue: queue.PriorityQueue):
        super().__init__()
        self.task_queue = task_queue

    def run(self):
        print('Consumer: Running')
        while True:
            try:
                priority, task = self.task_queue.get(timeout=1)
                if task is None:
                    self.task_queue.task_done()
                    break
                print(f'>running {task}.      sleep({task.args[0]})')
                task.execute()
                self.task_queue.task_done()
            except queue.Empty:
                break
        print('Consumer: Done')


def main():
    task_queue = queue.PriorityQueue()
    num_tasks = 10

    producer = Producer(task_queue, num_tasks)
    consumer = Consumer(task_queue)

    producer.start()
    producer.join()

    consumer.start()
    task_queue.put((float('-inf'), None))  # TODO цель этого была расположить запись в конце всех задач, значить надо
                                           #  указать +inf, ну или значение заведом больше любого возможного приоритета
    consumer.join()

    task_queue.join()


if __name__ == '__main__':
    main()
