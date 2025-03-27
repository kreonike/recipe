import subprocess


def process_count(user_name: str) -> int:
    """
    Возвращает количество процессов, запущенных из-под текущего пользователя `username`.
    Использует команду `ps` с флагами `-u` и `-o` для фильтрации по пользователю и подсчета строк.
    """
    try:
        result = subprocess.run(
            ['pgrep', '-u', user_name, '-c'], capture_output=True, text=True, check=True
        )
        return int(result.stdout.strip())
    except subprocess.CalledProcessError:
        result = subprocess.run(
            ['ps', '-u', user_name, '-o', 'pid='],
            capture_output=True,
            text=True,
            check=True,
        )
        count = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        return count


def total_memory_usage(pid: int) -> float:
    """
    Возвращает суммарное потребление памяти древа процессов с корнем `root_pid` в процентах.
    Использует команду `ps` с флагами `--ppid` и `-o` для получения памяти поддерева процессов.
    """
    try:
        pids = (
            subprocess.run(
                ['ps', '--ppid', str(pid), '-o', 'pid=', '--no-headers'],
                capture_output=True,
                text=True,
                check=True,
            )
            .stdout.strip()
            .split()
        )
        pids.append(str(pid))

        result = subprocess.run(
            ['ps', '-p', ','.join(pids), '-o', '%mem=', '--no-headers'],
            capture_output=True,
            text=True,
            check=True,
        )

        total = sum(
            float(line.strip()) for line in result.stdout.split('\n') if line.strip()
        )
        return total
    except subprocess.CalledProcessError:
        return 0.0


if __name__ == '__main__':
    username = subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip()
    print(f'Количество процессов пользователя {username}: {process_count(username)}')

    root_pid = 1  # Пример: PID init/systemd
    print(f'Суммарное использование памяти: {total_memory_usage(root_pid):.2f}%')


#####
# python3 test.py
# Количество процессов пользователя root: 323
# Суммарное использование памяти: 1.60%
