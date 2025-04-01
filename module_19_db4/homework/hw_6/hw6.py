import os
import sqlite3

from tabulate import tabulate


def analyze_read_study_assignments():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    db_path = os.path.join(grandparent_dir, 'homework.db')

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            query = '''
            SELECT 
                ROUND(AVG(avg_grade), 2) AS overall_avg_grade,
                COUNT(*) AS assignments_count,
                SUM(students_count) AS total_students
            FROM (
                SELECT 
                    a.assisgnment_id,
                    a.assignment_text,
                    AVG(ag.grade) AS avg_grade,
                    COUNT(DISTINCT ag.student_id) AS students_count
                FROM 
                    assignments a
                JOIN 
                    assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
                WHERE 
                    a.assignment_text LIKE '%прочитать%' 
                    OR a.assignment_text LIKE '%выучить%'
                GROUP BY 
                    a.assisgnment_id, a.assignment_text
            ) AS read_study_assignments;
            '''

            cursor.execute(query)
            result = cursor.fetchone()

            if not result:
                print(
                    'Не найдено заданий с ключевыми словами "прочитать" или "выучить".'
                )
                return

            headers = ['Средняя оценка', 'Количество заданий', 'Всего студентов']
            print('\nАнализ заданий типа "прочитать/выучить":')
            print(tabulate([result], headers=headers, tablefmt='grid', floatfmt='.2f'))

    except sqlite3.Error as e:
        print(f'Ошибка при работе с базой данных: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    print('Анализ заданий "прочитать/выучить"')
    print('=' * 50)
    analyze_read_study_assignments()
