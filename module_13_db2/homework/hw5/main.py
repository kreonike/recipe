import random
import sqlite3


def generate_test_data(cursor_: sqlite3.Cursor, number_of_groups_: int) -> None:
    if number_of_groups_ < 4 or number_of_groups_ > 16:
        raise ValueError("Количество групп должно быть от 4 до 16.")

    cursor_.execute("DELETE FROM uefa_commands")
    cursor_.execute("DELETE FROM uefa_draw")

    countries = [
        "Россия",
        "Германия",
        "Испания",
        "Франция",
        "Англия",
        "Италия",
        "Португалия",
        "Нидерланды",
        "Бельгия",
        "Украина",
        "Шотландия",
        "Швейцария",
        "Турция",
        "Австрия",
        "Дания",
        "Чехия",
    ]
    team_names = [
        "Спартак",
        "Динамо",
        "ЦСКА",
        "Локомотив",
        "Барселона",
        "Реал Мадрид",
        "Бавария",
        "Дортмунд",
        "Ливерпуль",
        "Манчестер Юнайтед",
        "Челси",
        "Арсенал",
        "Ювентус",
        "Милан",
        "Интер",
        "ПСЖ",
    ]

    teams = []
    team_id = 1

    for i in range(number_of_groups_):
        country = random.choice(countries)
        name = f"{random.choice(team_names)} {country}"
        teams.append((team_id, name, country, "сильная"))
        team_id += 1

    for i in range(number_of_groups_ * 2):
        country = random.choice(countries)
        name = f"{random.choice(team_names)} {country}"
        teams.append((team_id, name, country, "средняя"))
        team_id += 1

    for i in range(number_of_groups_):
        country = random.choice(countries)
        name = f"{random.choice(team_names)} {country}"
        teams.append((team_id, name, country, "слабая"))
        team_id += 1

    cursor_.executemany(
        "INSERT INTO uefa_commands (id, name, country, level) VALUES (?, ?, ?, ?)",
        teams,
    )

    strong_teams = [team[0] for team in teams if team[3] == "сильная"]
    average_teams = [team[0] for team in teams if team[3] == "средняя"]
    weak_teams = [team[0] for team in teams if team[3] == "слабая"]

    random.shuffle(strong_teams)
    random.shuffle(average_teams)
    random.shuffle(weak_teams)

    draw_results = []
    for group in range(1, number_of_groups_ + 1):
        if strong_teams:
            draw_results.append((strong_teams.pop(), group))
        for _ in range(2):
            if average_teams:
                draw_results.append((average_teams.pop(), group))
        if weak_teams:
            draw_results.append((weak_teams.pop(), group))

    cursor_.executemany(
        "INSERT INTO uefa_draw (command_id, group_id) VALUES (?, ?)", draw_results
    )


if __name__ == '__main__':
    number_of_groups: int = int(input('Введите количество групп (от 4 до 16): '))
    with sqlite3.connect('../homework.db') as conn:
        cursor: sqlite3.Cursor = conn.cursor()
        generate_test_data(cursor, number_of_groups)
        conn.commit()
