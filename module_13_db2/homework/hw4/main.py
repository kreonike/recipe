import sqlite3


def ivan_soviet_the_most_effective(
    cursor_: sqlite3.Cursor,
    name_: str,
) -> None:
    cursor_.execute(
        '''
        SELECT salary FROM table_effective_manager
        WHERE name = 'Иван Совин'
    '''
    )
    ivan_salary = cursor_.fetchone()[0]

    cursor_.execute(
        '''
        SELECT salary FROM table_effective_manager
        WHERE name = ?
    ''',
        (name_,),
    )
    employee = cursor_.fetchone()

    if employee is None:
        print(f'Сотрудник {name_} не найден в базе данных')
        return

    employee_salary = employee[0]

    if name_ == 'Иван Совин':
        print('Иван Совин всегда эффективен!')
        return

    if employee_salary <= ivan_salary:
        new_salary = employee_salary * 1.1
        cursor_.execute(
            '''
            UPDATE table_effective_manager
            SET salary = ?
            WHERE name = ?
        ''',
            (new_salary, name_),
        )
        print(f'Зарплата сотрудника {name_} повышена до {new_salary:.2f}')
    else:
        cursor_.execute(
            '''
            DELETE FROM table_effective_manager
            WHERE name = ?
        ''',
            (name_,),
        )
        print(f'Сотрудник {name_} уволен за превышение зарплаты Ивана Совина')


if __name__ == '__main__':
    name: str = input('Введите имя сотрудника: ')
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        ivan_soviet_the_most_effective(cursor, name)
        conn.commit()
