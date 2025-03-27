import sys
import time
from threading import Semaphore, Thread

sem: Semaphore = Semaphore()
stop_threads = False


def fun1():
    while not stop_threads:
        sem.acquire()
        print(1)
        sem.release()
        time.sleep(0.25)


def fun2():
    while not stop_threads:
        sem.acquire()
        print(2)
        sem.release()
        time.sleep(0.25)


t1: Thread = Thread(target=fun1)  # TODO добавьте параметр daemon=True
t2: Thread = Thread(target=fun2)  # TODO Аналогично предыдущему
# TODO создание потоков работающих в фоновом режиме https://codechick.io/tutorials/python/python-daemon-threads


try:
    t1.start()
    t2.start()
    while True:  # TODO вместо цикла, просто джойните потоки тут, ведь join это блокирующий метод
        time.sleep(0.1)
except KeyboardInterrupt:
    print('\nReceived keyboard interrupt, quitting threads.')
    stop_threads = True
    t1.join()
    t2.join()
    sys.exit(0)
