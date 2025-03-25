import sqlite3
import threading
import time
from typing import List, Dict

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


def single_threaded_version() -> float:
    start_time = time.time()
    for i in range(1, NUM_CHARACTERS + 1):
        character = fetch_character_data(i)
        save_character_to_db(character)
    end_time = time.time()
    return end_time - start_time


def multi_threaded_version() -> float:
    start_time = time.time()
    threads: List[threading.Thread] = []

    def process_character(character_id: int) -> None:
        character = fetch_character_data(character_id)
        save_character_to_db(character)

    for i in range(1, NUM_CHARACTERS + 1):
        thread = threading.Thread(target=process_character, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    return end_time - start_time


def main() -> None:
    create_database()

    single_time = single_threaded_version()
    print(f'однопоточный режим: {single_time:.2f} seconds')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM characters')
    conn.commit()
    conn.close()

    multi_time = multi_threaded_version()
    print(f'многопоточный режим: {multi_time:.2f} секунд')

    print('\n')
    print(f'однопоточный режим: {single_time:.2f} секунд')
    print(f'многопоточный режим: {multi_time:.2f} секунд')
    print(f'разница: {single_time / multi_time:.2f}x')


if __name__ == '__main__':
    main()
