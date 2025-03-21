"""
Помимо того чтобы логи писать, нужно их ещё и уметь читать,
иначе мы будем как в известном анекдоте, писателями, а не читателями.

Для вас мы написали простую функцию обхода binary tree по уровням.
Также в репозитории есть файл с логами, написанными этой программой.

Напишите функцию restore_tree, которая принимает на вход путь до файла с логами
    и восстанавливать исходное BinaryTree.

Функция должна возвращать корень восстановленного дерева

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    pass

Примечание: гарантируется, что все значения, хранящиеся в бинарном дереве уникальны
"""

import logging
from dataclasses import dataclass
from typing import Optional, Dict
from common import configure_logging, JsonAdapter

@dataclass
class BinaryTreeNode:
    val: int
    left: Optional["BinaryTreeNode"] = None
    right: Optional["BinaryTreeNode"] = None

    def __repr__(self):
        return f"<BinaryTreeNode[{self.val}]>"

def restore_tree(path_to_log_file: str) -> BinaryTreeNode:
    configure_logging(level=logging.DEBUG)
    logger = JsonAdapter(logging.getLogger("restore_tree"))

    nodes: Dict[int, BinaryTreeNode] = {}
    root = None

    with open(path_to_log_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        if "Visiting" in line:
            node_value = int(line.split("Visiting <BinaryTreeNode[")[1].split("]>")[0])
            if node_value not in nodes:
                nodes[node_value] = BinaryTreeNode(val=node_value)
            current_node = nodes[node_value]

            if root is None:
                root = current_node
                logger.info(f"Root node found: {root}")

        elif "left is not empty" in line:
            left_value = int(line.split("Adding <BinaryTreeNode[")[1].split("]>")[0])
            if left_value not in nodes:
                nodes[left_value] = BinaryTreeNode(val=left_value)
            current_node.left = nodes[left_value]
            logger.debug(f"Added left child {left_value} to node {current_node.val}")

        elif "right is not empty" in line:
            right_value = int(line.split("Adding <BinaryTreeNode[")[1].split("]>")[0])
            if right_value not in nodes:
                nodes[right_value] = BinaryTreeNode(val=right_value)
            current_node.right = nodes[right_value]
            logger.debug(f"Added right child {right_value} to node {current_node.val}")

    logger.info("Tree restoration completed")
    return root

if __name__ == "__main__":
    restored_root = restore_tree("walk_log_4.txt")
    def print_tree(node: Optional[BinaryTreeNode], level: int = 0):
        if node is not None:
            print_tree(node.right, level + 1)
            print(' ' * 4 * level + '->', node.val)
            print_tree(node.left, level + 1)

    print_tree(restored_root)