import sqlite3


def create_database():
    with open('create_schema.sql', 'r') as sql_file:
        sql_script = sql_file.read()

    with sqlite3.connect('cinema.db') as conn:
        cursor = conn.cursor()

        cursor.executescript(sql_script)
        conn.commit()

        print('База данных успешно создана!')


if __name__ == '__main__':
    create_database()
