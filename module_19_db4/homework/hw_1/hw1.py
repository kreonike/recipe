import os
import sqlite3

from tabulate import tabulate


def analyze_teachers_assignments_difficulty():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)  # Два уровня выше
    db_path = os.path.join(grandparent_dir, 'homework.db')

    try:
        if not os.path.exists(db_path):
            print(f'Ошибка: файл базы данных не найден по пути: {db_path}')
            print('Проверьте расположение файла homework.db')
            return

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Проверка существования таблицы teachers
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='teachers';"
            )
            if not cursor.fetchone():
                print('Ошибка: таблица teachers не найдена в базе данных')
                return

            query = '''
            SELECT 
                t.teacher_id,
                t.full_name AS teacher_name,
                ROUND(AVG(ag.grade), 2) AS average_grade,
                COUNT(DISTINCT a.assisgnment_id) AS assignments_count,
                COUNT(ag.grade_id) AS grades_count
            FROM 
                teachers t
            JOIN 
                assignments a ON t.teacher_id = a.teacher_id
            JOIN 
                assignments_grades ag ON a.assisgnment_id = ag.assisgnment_id
            GROUP BY 
                t.teacher_id, t.full_name
            ORDER BY 
                average_grade ASC;
            '''

            cursor.execute(query)
            results = cursor.fetchall()

            if not results:
                print('В базе данных нет записей для анализа.')
                return

            headers = ['ID', 'Преподаватель', 'Средний балл', 'Заданий', 'Оценок']
            print('\nПреподаватели с самыми сложными заданиями (по среднему баллу):')
            print(tabulate(results, headers=headers, tablefmt='grid', floatfmt='.2f'))

            hardest = min(results, key=lambda x: x[2])
            easiest = max(results, key=lambda x: x[2])
            print(
                f'\nСамый строгий преподаватель: {hardest[1]} (средний балл: {hardest[2]})'
            )
            print(
                f'Самый лояльный преподаватель: {easiest[1]} (средний балл: {easiest[2]})'
            )

    except sqlite3.Error as e:
        print(f'Ошибка SQLite: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


if __name__ == '__main__':
    print('Анализ сложности заданий преподавателей')
    print('=' * 50)
    analyze_teachers_assignments_difficulty()
