import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ Создает соединение с SQLite базой данных """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


def analyze_island_poverty(conn):
    """ Выполняет анализ данных по острову N """

    query1 = '''
    SELECT COUNT(*) 
    FROM salaries 
    WHERE salary < 5000;
    '''

    query2 = '''
    SELECT AVG(salary) 
    FROM salaries;
    '''

    query3 = '''
    SELECT salary 
    FROM salaries 
    ORDER BY salary 
    LIMIT 1 
    OFFSET (SELECT COUNT(*) FROM salaries) / 2;
    '''

    query4 = '''
    WITH total_count AS (
        SELECT COUNT(*) AS cnt FROM salaries
    ),
    top10 AS (
        SELECT salary 
        FROM salaries, total_count
        ORDER BY salary DESC 
        LIMIT (SELECT cnt FROM total_count) / 10
    ),
    bottom90 AS (
        SELECT salary 
        FROM salaries, total_count
        ORDER BY salary ASC 
        LIMIT (SELECT cnt FROM total_count) * 9 / 10
    )
    SELECT ROUND(100.0 * (SELECT SUM(salary) FROM top10) / 
                  (SELECT SUM(salary) FROM bottom90), 2) 
    AS inequality_index;
    '''

    try:
        cur = conn.cursor()

        cur.execute(query1)
        poor_count = cur.fetchone()[0]

        cur.execute(query2)
        avg_salary = round(cur.fetchone()[0], 2)

        cur.execute(query3)
        median_salary = cur.fetchone()[0]

        cur.execute(query4)
        inequality = cur.fetchone()[0]

        # Вывод результатов
        print(f'1. Количество людей за чертой бедности: {poor_count}')
        print(f'2. Средняя зарплата по острову: {avg_salary} гульденов')
        print(f'3. Медианная зарплата по острову: {median_salary} гульденов')
        print(f'4. Коэффициент социального неравенства F: {inequality}%')

    except Error as e:
        print(f'Ошибка при выполнении запроса: {e}')


def main():
    database = 'hw_4_database.db'

    conn = create_connection(database)

    if conn is not None:
        analyze_island_poverty(conn)
        conn.close()
    else:
        print('Ошибка! Не удалось подключиться к базе данных.')


if __name__ == '__main__':
    main()