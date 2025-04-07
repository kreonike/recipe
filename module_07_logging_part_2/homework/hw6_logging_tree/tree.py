import logging.config
from logging_config import LOGGING_CONFIG
import logging_tree

logging.config.dictConfig(LOGGING_CONFIG)

tree_structure = logging_tree.format.build_description()

with open("logging_tree.txt", "w", encoding="utf-8") as file:
    file.write(tree_structure)

print(f" структура записана в файл logging_tree.txt")
