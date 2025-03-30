import sqlite3


def execute_query(query_file, output_file):
    with open(query_file, 'r') as f:
        query = f.read()

    with sqlite3.connect('hw.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

    with open(output_file, 'w') as f:
        for row in results:
            f.write(str(row) + '\n')


if __name__ == '__main__':
    queries = {
        '2_1.sql': 'output_1.txt',
        '2_2.sql': 'output_2.txt',
        '2_3.sql': 'output_3.txt',
        '2_4.sql': 'output_4.txt',
        '2_5.sql': 'output_5.txt',
    }

    for query_file, output_file in queries.items():
        try:
            execute_query(query_file, output_file)
            print(f'Query {query_file} executed, results saved to {output_file}')
        except Exception as e:
            print(f'Error executing {query_file}: {str(e)}')
