#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict, Tuple
import pydot
from helpers import get_suffixes

@dataclass
class Node:
    TERMINAL = "$"

    def __init__(self, id: str = "root", parent: Tuple["Node", str] | None = None):
        self.parent = parent
        self.id: str = id

        self.children: Dict[str, "Node"] = {}

    def get_max_depth(self) -> int:
        if len(self.children) == 0:
            return 0
        else:
            return max([child.get_max_depth() for child in self.children.values()]) + 1

    def get_children(self, depth=0) -> List["Node"]:
        if depth <= 0:
            return [self]
        else:
            result = []
            for child in self.children.values():
                result.extend(child.get_children(depth - 1))
            return result

    def get_level(self):
        if self.parent is None:
            return 0
        else:
            return self.parent[0].get_level() + 1

    @staticmethod
    def build(pattern: str) -> "Node":
        root: Node = Node()
        for pattern in get_suffixes(pattern + Node.TERMINAL):
            node: Node = root
            for i in range(len(pattern)):
                char: str = pattern[i]
                parent: Node = node

                nodeOrNone: Node | None = parent.children.get(char, None)

                if nodeOrNone is None:
                    node = Node(pattern[: i + 1], (parent, char))
                    parent.children[char] = node
                else:
                    node = nodeOrNone

        return root

    def tree(self, path: str = "tree.png") -> None:
        graph = pydot.Dot(graph_type="digraph")

        for depth in range(self.get_max_depth() + 1):
            for node in self.get_children(depth):
                graph.add_node(pydot.Node(node.id))

                for char, child in node.children.items():
                    graph.add_edge(pydot.Edge(node.id, child.id, label=char))

        graph.write_png(path)

if __name__ == "__main__":
    root = Node.build("abbaba")

    root.tree()