import csv
import sqlite3


def delete_wrong_fees(cursor_: sqlite3.Cursor, wrong_fees_file: str) -> None:
    with open(wrong_fees_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                timestamp, car_number = row[0], row[1]
                cursor_.execute(
                    """
                    DELETE FROM table_fees
                    WHERE timestamp = ? AND car_number = ?
                """,
                    (timestamp, car_number),
                )


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        delete_wrong_fees(cursor, '../wrong_fees.csv')
        conn.commit()
