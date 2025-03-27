import sqlite3


def check_if_vaccine_has_spoiled(cursor_: sqlite3.Cursor, truck_number_: str) -> bool:
    cursor_.execute(
        """
        SELECT temperature 
        FROM table_truck_with_vaccine 
        WHERE truck_number = ?
    """,
        (truck_number_,),
    )
    temperatures = cursor_.fetchall()

    violation_count = 0
    for temp in temperatures:
        if not (-20 <= temp[0] <= -16):
            violation_count += 1
            if violation_count >= 3:
                return True
    return False


if __name__ == '__main__':
    truck_number: str = input('Введите номер грузовика: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        spoiled: bool = check_if_vaccine_has_spoiled(cursor, truck_number)
        print('Испортилась' if spoiled else 'Не испортилась')
        conn.commit()
