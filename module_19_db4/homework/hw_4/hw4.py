import os
import sqlite3

from tabulate import tabulate


def calculate_late_assignments_stats():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    db_path = os.path.join(grandparent_dir, 'homework.db')

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='assignments';"
            )
            if not cursor.fetchone():
                print("Ошибка: таблица 'assignments' не найдена")
                return

            query = '''
            SELECT
                sg.group_id AS class_id,
                COUNT(DISTINCT s.student_id) AS students_count,
                ROUND(AVG(late_count), 2) AS avg_late_assignments,
                MAX(late_count) AS max_late_assignments,
                MIN(late_count) AS min_late_assignments
            FROM
                students_groups sg
            JOIN
                students s ON sg.group_id = s.group_id
            LEFT JOIN (
                SELECT
                    ag.student_id,
                    COUNT(*) AS late_count
                FROM
                    assignments_grades ag
                JOIN
                    assignments a ON ag.assisgnment_id = a.assisgnment_id
                WHERE
                    ag.date > a.due_date
                GROUP BY
                    ag.student_id
            ) late ON s.student_id = late.student_id
            GROUP BY
                sg.group_id
            ORDER BY
                sg.group_id;
            '''

            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print('В базе данных нет данных для анализа.')
                return

            headers = [
                'ID класса',
                'Кол-во студентов',
                'Среднее просрочено',
                'Макс просрочено',
                'Мин просрочено',
            ]
            print('\nСтатистика просроченных заданий по классам:')
            print(tabulate(results, headers=headers, tablefmt='grid', floatfmt='.2f'))

    except sqlite3.Error as e:
        print(f'Ошибка при работе с базой данных: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    print('Анализ просроченных заданий по классам')
    print('=' * 50)
    calculate_late_assignments_stats()
