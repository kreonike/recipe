import sqlite3


def check_if_vaccine_has_spoiled(cursor_: sqlite3.Cursor, truck_number_: str) -> bool:
    cursor_.execute(
        """
        SELECT COUNT(*) 
        FROM table_truck_with_vaccine 
        WHERE truck_number = ? 
        AND temperature NOT BETWEEN -20 AND -16
        HAVING COUNT(*) >= 3
        """,
        (truck_number_,),
    )
    result = cursor_.fetchone()
    return result is not None  # Если результат есть, значит, есть ≥3 нарушений


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
