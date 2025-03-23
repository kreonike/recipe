import configparser


def ini_to_dict(ini_file):
    """
    Конвертирует INI-файл в словарь.
    :param ini_file: Путь к INI-файлу.
    :return: Словарь с конфигурацией.
    """
    config = configparser.ConfigParser(interpolation=None)  # Отключаем интерполяцию
    config.read(ini_file)

    # Преобразуем INI-файл в словарь
    config_dict = {}
    for section in config.sections():
        config_dict[section] = {}
        for key, value in config[section].items():
            config_dict[section][key] = value

    return config_dict


def write_dict_to_py(dict_data, output_file):
    """
    Записывает словарь в Python-файл.
    :param dict_data: Словарь с конфигурацией.
    :param output_file: Путь к выходному файлу.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("LOGGING_CONFIG = {\n")
        for section, options in dict_data.items():
            f.write(f'    "{section}": {{\n')
            for key, value in options.items():
                value = value.replace('"', '\\"')
                f.write(f'        "{key}": "{value}",\n')
            f.write("    },\n")
        f.write("}\n")


ini_file = "logging_conf.ini"

config_dict = ini_to_dict(ini_file)

write_dict_to_py(config_dict, "dict_config.py")

print("Конфигурация успешно записана в dict_config.py")
# TODO задание по конвертации со звездочкой, не обязательное.
#  Самое простое решение использовать тот же configparser:
# import configparser
# import json
# config_object = configparser.RawConfigParser()  # or use interpolation=None for just ConfigParser
# with open("logging_conf.ini","r") as file:
#     config_object.read_file(file)
#     output_dict = {s: dict(config_object.items(s)) for s in config_object.sections()}
# print("Dictionary config:\n", json.dumps(output_dict, indent=4))
