import os
import sqlite3

from tabulate import tabulate


def get_top_students():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    db_path = os.path.join(grandparent_dir, 'homework.db')

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            query = '''
            SELECT 
                s.student_id,
                s.full_name AS student_name,
                ROUND(AVG(ag.grade), 2) AS average_grade,
                COUNT(ag.grade_id) AS grades_count
            FROM 
                students s
            JOIN 
                assignments_grades ag ON s.student_id = ag.student_id
            GROUP BY 
                s.student_id, s.full_name
            HAVING
                COUNT(ag.grade_id) >= 3  -- Учитываем только учеников с 3+ оценками
            ORDER BY 
                average_grade DESC
            LIMIT 10;
            '''

            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print('В базе данных нет записей для анализа.')
                return

            headers = ['ID', 'Ученик', 'Средний балл', 'Кол-во оценок']
            print('\nТоп-10 лучших учеников:')
            print(tabulate(results, headers=headers, tablefmt='grid', floatfmt='.2f'))

    except sqlite3.Error as e:
        print(f'Ошибка при работе с базой данных: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    print('Выбор лучших учеников для награждения')
    print('=' * 50)
    get_top_students()
