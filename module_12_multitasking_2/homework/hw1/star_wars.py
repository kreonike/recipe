import sqlite3
import time
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool
from typing import Dict

import requests

# Константы
SWAPI_URL = 'https://swapi.dev/api/people/'
DB_NAME = 'star_wars_characters.db'
NUM_CHARACTERS = 20


def create_database() -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age TEXT,
            gender TEXT
        )
    '''
    )
    conn.commit()
    conn.close()


def fetch_character_data(character_id: int) -> Dict[str, str]:
    response = requests.get(f'{SWAPI_URL}{character_id}/')
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data.get('name', 'Unknown'),
            'age': data.get('birth_year', 'Unknown'),
            'gender': data.get('gender', 'Unknown'),
        }
    return {'name': 'Unknown', 'age': 'Unknown', 'gender': 'Unknown'}


def save_character_to_db(character: Dict[str, str]) -> None:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO characters (name, age, gender)
        VALUES (?, ?, ?)
    ''',
        (character['name'], character['age'], character['gender']),
    )
    conn.commit()
    conn.close()


def process_character(character_id: int) -> None:
    character = fetch_character_data(character_id)
    save_character_to_db(character)


def single_threaded_version() -> float:
    start_time = time.time()
    for i in range(1, NUM_CHARACTERS + 1):
        process_character(i)
    end_time = time.time()
    return end_time - start_time


def multi_process_version() -> float:
    start_time = time.time()
    with Pool() as pool:
        pool.map(process_character, range(1, NUM_CHARACTERS + 1))
    end_time = time.time()
    return end_time - start_time


def multi_thread_version() -> float:
    start_time = time.time()
    with ThreadPool() as pool:
        pool.map(process_character, range(1, NUM_CHARACTERS + 1))
    end_time = time.time()
    return end_time - start_time


def main() -> None:
    create_database()

    # Очистка таблицы перед тестами
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM characters')
    conn.commit()
    conn.close()

    single_time = single_threaded_version()
    print(f'Однопоточный режим: {single_time:.2f} секунд')

    # Очистка таблицы перед тестами
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM characters')
    conn.commit()
    conn.close()

    multi_process_time = multi_process_version()
    print(f'Многопроцессорный режим (Pool): {multi_process_time:.2f} секунд')

    # Очистка таблицы перед тестами
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM characters')
    conn.commit()
    conn.close()

    multi_thread_time = multi_thread_version()
    print(f'Многопоточный режим (ThreadPool): {multi_thread_time:.2f} секунд')

    print('\nСравнение результатов:')
    print(f'Однопоточный режим: {single_time:.2f} секунд')
    print(f'Многопроцессорный режим (Pool): {multi_process_time:.2f} секунд')
    print(f'Многопоточный режим (ThreadPool): {multi_thread_time:.2f} секунд')
    print(f'Ускорение Pool: {single_time / multi_process_time:.2f}x')
    print(f'Ускорение ThreadPool: {single_time / multi_thread_time:.2f}x')


if __name__ == '__main__':
    main()
