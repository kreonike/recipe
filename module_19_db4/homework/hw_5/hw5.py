import os
import sqlite3

from tabulate import tabulate


def analyze_groups_performance():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)
    db_path = os.path.join(grandparent_dir, 'homework.db')

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            query = '''
            WITH submission_counts AS (
                SELECT 
                    student_id,
                    assisgnment_id,
                    COUNT(*) AS attempts_count
                FROM 
                    assignments_grades
                GROUP BY 
                    student_id, assisgnment_id
            )
            SELECT 
                sg.group_id AS group_id,
                COUNT(DISTINCT s.student_id) AS total_students,
                ROUND(AVG(ag.grade), 2) AS avg_grade,
                SUM(CASE WHEN ag.grade < 4 THEN 1 ELSE 0 END) AS failed_assignments,
                SUM(CASE WHEN ag.date > a.due_date THEN 1 ELSE 0 END) AS late_submissions,
                SUM(CASE WHEN sc.attempts_count > 1 THEN sc.attempts_count - 1 ELSE 0 END) AS resubmissions
            FROM 
                students_groups sg
            JOIN 
                students s ON sg.group_id = s.group_id
            LEFT JOIN 
                assignments_grades ag ON s.student_id = ag.student_id
            LEFT JOIN 
                assignments a ON ag.assisgnment_id = a.assisgnment_id
            LEFT JOIN
                submission_counts sc ON s.student_id = sc.student_id AND ag.assisgnment_id = sc.assisgnment_id
            GROUP BY 
                sg.group_id
            ORDER BY 
                avg_grade DESC;
            '''

            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print('В базе данных нет данных для анализа.')
                return

            headers = [
                'ID группы',
                'Всего учеников',
                'Средний балл',
                'Не сдано работ',
                'Просрочено дедлайнов',
                'Повторных попыток',
            ]
            print('\nАнализ успеваемости по группам:')
            print(tabulate(results, headers=headers, tablefmt='grid', floatfmt='.2f'))

    except sqlite3.Error as e:
        print(f'Ошибка при работе с базой данных: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    print('Комплексный анализ групп')
    print('=' * 50)
    analyze_groups_performance()
