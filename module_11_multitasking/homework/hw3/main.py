import logging
import random
import threading
import time
from typing import List

TOTAL_TICKETS: int = 10
MAX_TICKETS: int = 100

logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger(__name__)


class Seller(threading.Thread):
    def __init__(
        self,
        semaphore: threading.Semaphore,
        director_event: threading.Event,
        sellers_count: int,
    ) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.director_event: threading.Event = director_event
        self.sellers_count: int = sellers_count
        self.tickets_sold: int = 0
        logger.info('Seller started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        is_running: bool = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                if (
                    TOTAL_TICKETS <= self.sellers_count
                    and not self.director_event.is_set()
                ):
                    self.director_event.set()
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.name} sold one; {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self) -> None:
        time.sleep(random.randint(0, 1))


class Director(threading.Thread):
    def __init__(
        self, semaphore: threading.Semaphore, director_event: threading.Event
    ) -> None:
        super().__init__()
        self.sem: threading.Semaphore = semaphore
        self.director_event: threading.Event = director_event
        logger.info('Director started work')

    def run(self) -> None:
        global TOTAL_TICKETS
        while True:
            self.director_event.wait()
            with self.sem:
                if TOTAL_TICKETS > 0:
                    added_tickets = random.randint(5, 10)
                    if TOTAL_TICKETS + added_tickets > MAX_TICKETS:
                        added_tickets = MAX_TICKETS - TOTAL_TICKETS
                    if added_tickets > 0:
                        TOTAL_TICKETS += added_tickets
                        logger.info(
                            f'Director added {added_tickets} tickets; Total now: {TOTAL_TICKETS}'
                        )
                    else:
                        logger.info('No more tickets can be added. Maximum reached.')
                self.director_event.clear()


def main() -> None:
    semaphore: threading.Semaphore = threading.Semaphore()
    director_event: threading.Event = threading.Event()

    director = Director(semaphore, director_event)
    director.start()

    sellers_count = 4
    sellers: List[Seller] = []
    for _ in range(sellers_count):
        seller = Seller(semaphore, director_event, sellers_count)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()

    director_event.set()
    director.join()

    logger.info(f'All tickets sold. Total tickets: {TOTAL_TICKETS}')


if __name__ == '__main__':
    main()
