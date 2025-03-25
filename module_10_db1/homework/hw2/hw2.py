import sqlite3


def count_phone_colors(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT 
            p.colour AS color,
            COUNT(*) AS purchase_count
        FROM 
            table_checkout c
        JOIN 
            table_phones p ON c.phone_id = p.id
        GROUP BY 
            p.colour
        ORDER BY 
            purchase_count DESC
    '''
    )

    results = cursor.fetchall()

    print('Количество покупок по цветам:')
    for row in results:
        print(f'{row[0]}: {row[1]} покупок')

    conn.close()


# Запускаем анализ
if __name__ == '__main__':
    count_phone_colors('hw_2_database.db')
