import sqlite3
from datetime import datetime, timedelta


def update_work_schedule(cursor: sqlite3.Cursor) -> None:
    sport_days = {
        0: 'футбол',
        1: 'хоккей',
        2: 'шахматы',
        3: 'SUP-сёрфинг',
        4: 'бокс',
        5: 'Dota2',
        6: 'шахбокс',
    }

    cursor.execute(
        'SELECT rowid, employee_id, date, sport FROM table_friendship_schedule'
    )
    schedule = cursor.fetchall()

    for rowid, employee_id, date_str, sport in schedule:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        weekday = date.weekday()

        if sport == sport_days.get(weekday):
            for delta in range(1, 8):
                new_date = date + timedelta(days=delta)
                new_weekday = new_date.weekday()
                if sport != sport_days.get(new_weekday):
                    cursor.execute(
                        '''
                        UPDATE table_friendship_schedule
                        SET date = ?
                        WHERE rowid = ?
                    ''',
                        (new_date.strftime('%Y-%m-%d'), rowid),
                    )
                    break


if __name__ == '__main__':
    with sqlite3.connect('../homework.db') as conn:
        cursor = conn.cursor()
        update_work_schedule(cursor)
        conn.commit()
