import datetime
import sqlite3


def log_bird(
    cursor: sqlite3.Cursor,
    bird_name: str,
    date_time: str,
) -> None:
    cursor.execute(
        '''
        INSERT INTO table_birds (time, bird_name)
        VALUES (?, ?)
    ''',
        (date_time, bird_name),
    )


def check_if_such_bird_already_seen(cursor: sqlite3.Cursor, bird_name: str) -> bool:
    cursor.execute(
        '''
        SELECT EXISTS (
            SELECT 1 
            FROM table_birds 
            WHERE bird_name = ?
        )
    ''',
        (bird_name,),
    )
    return cursor.fetchone()[0] == 1


if __name__ == '__main__':
    print('Программа помощи')
    name: str = input('Пожалуйста введите имя птицы\n> ')
    count_str: str = input('Сколько птиц вы увидели?\n> ')
    count: int = int(count_str)
    right_now: str = datetime.datetime.utcnow().isoformat()

    with sqlite3.connect('../homework.db') as connection:
        cursor: sqlite3.Cursor = connection.cursor()
        log_bird(cursor, name, right_now)

        if check_if_such_bird_already_seen(cursor, name):
            print('Такую птицу мы уже наблюдали!')
