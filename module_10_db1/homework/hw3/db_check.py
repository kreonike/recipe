import sqlite3

with sqlite3.connect('hw_3_database.db') as conn:
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM table_1')
    count_table_1 = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM table_2')
    count_table_2 = cursor.fetchone()[0]

    cursor.execute('SELECT COUNT(*) FROM table_3')
    count_table_3 = cursor.fetchone()[0]

    print(f'Количество записей: table_1 - {count_table_1}, table_2 - {count_table_2}, table_3 - {count_table_3}')

    cursor.execute('SELECT COUNT(DISTINCT value) FROM table_1')
    unique_table_1 = cursor.fetchone()[0]
    print(f'Уникальных записей в table_1: {unique_table_1}')

    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT DISTINCT value FROM table_1
            INTERSECT
            SELECT DISTINCT value FROM table_2
        )
    """)
    table_1_in_table_2 = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM (
            SELECT DISTINCT value FROM table_1
            INTERSECT
            SELECT DISTINCT value FROM table_2
            INTERSECT
            SELECT DISTINCT value FROM table_3
        )
    """)
    table_1_in_both = cursor.fetchone()[0]