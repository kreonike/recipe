import os
import sqlite3

from tabulate import tabulate


def find_easiest_teacher_students():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    db_path = os.path.join(grandparent_dir, 'homework.db')

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("PRAGMA table_info(assignments_grades);")
            columns = [column[1] for column in cursor.fetchall()]
            if 'grade' not in columns:
                print("Ошибка: столбец 'grade' не найден в таблице assignments_grades")
                print("Доступные столбцы:", ", ".join(columns))
                return

            nested_query = '''
            SELECT
                s.student_id,
                s.full_name AS student_name,
                ROUND(AVG(ag.grade), 2) AS student_avg_grade
            FROM
                students s
            JOIN
                assignments_grades ag ON s.student_id = ag.student_id
            WHERE
                s.group_id IN (
                    SELECT a.group_id
                    FROM assignments a
                    WHERE a.teacher_id = (
                        SELECT t.teacher_id
                        FROM teachers t
                        JOIN assignments a ON t.teacher_id = a.teacher_id
                        JOIN assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
                        GROUP BY t.teacher_id
                        ORDER BY AVG(ag.grade) DESC
                        LIMIT 1
                    )
                )
            GROUP BY
                s.student_id, s.full_name
            ORDER BY
                student_avg_grade DESC;
            '''

            cursor.execute(nested_query)
            results = cursor.fetchall()
            print_results(results)

    except sqlite3.Error as e:
        print(f'Ошибка при работе с базой данных: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


def print_results(results):
    if not results:
        print('Не найдено учеников для отображения.')
        return

    headers = ['ID', 'Ученик', 'Средний балл']
    print(tabulate(results, headers=headers, tablefmt='grid', floatfmt='.2f'))


if __name__ == '__main__':
    print('Ученики преподавателя с самыми простыми заданиями')
    print('=' * 50)
    find_easiest_teacher_students()
