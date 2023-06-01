#!/usr/bin/env python3

from typing import List, Dict, Tuple
import pydot

class Node:
    def __init__(self, id: str = "root", parent: Tuple["Node", str] = None):
        self.children: Dict[str, Node] = {}
        self.fail: Node = None
        self.leaf: bool = False
        self.parent = parent
        self.id: str = id

    def add_child(self, char, node):
        self.children[char] = node

    def get_child(self, term):
        if len((term)) == 1:
            return self.children.get(term)
        else:
            return self.children.get(term[0]).get_child(term[1:])

    def get_max_depth(self):
        if len(self.children) == 0:
            return 0
        else:
            return max([child.get_max_depth() for child in self.children.values()]) + 1

    def get_children(self, depth=0):
        if depth <= 0:
            return [self]
        else:
            result = []
            for child in self.children.values():
                result.extend(child.get_children(depth - 1))
            return result

    def set_fail(self, node):
        self.fail = node

    def set_leaf(self):
        self.leaf = True

    def get_parent(self):
        return self.parent[0]

    def get_parent_char(self):
        return self.parent[1]

    def get_level(self):
        if self.parent is None:
            return 0
        else:
            return self.parent[0].get_level() + 1

    @staticmethod
    def build(patterns: List[str]) -> "Node":
        root = Node()
        for pattern in patterns:
            node = root
            for i in range(len(pattern)):
                char = pattern[i]
                parent = node

                if parent.get_child(char) is None:
                    parent.add_child(char, Node(pattern[: i + 1], (parent, char)))

                node = parent.get_child(char)

            node.set_leaf()

        # Add fail links
        max_depth = max([len(pattern) for pattern in patterns]) + 1

        for length in range(1, max_depth):
            for node in root.get_children(length):
                parent = node.get_parent()
                parent_char = node.get_parent_char()

                w = parent.fail

                while w not in [None, root] and w.get_child(parent_char) is None:
                    w = w.fail

                if w is not None and w.get_child(parent_char) is not None:
                    node.set_fail(w.get_child(parent_char))
                else:
                    node.set_fail(root)

        return root

    def tree(self, path: str) -> None:
        graph = pydot.Dot(graph_type="digraph")

        for depth in range(self.get_max_depth() + 1):
            for node in self.get_children(depth):
                graph.add_node(pydot.Node(node.id, label=node.id))

                if node.fail is not None:
                    graph.add_edge(pydot.Edge(node.id, node.fail.id, style="dashed"))


                for char, child in node.children.items():
                    graph.add_edge(pydot.Edge(node.id, child.id, label=char))

        graph.write_png(path)

def aho_corasick(text: str, patterns: List[str], path: str = None) -> bool:
    root = Node.build(patterns)

    if path is not None:
        root.tree(path)

    result = []

    node = root
    i = 0

    while i < len(text):
        while node.get_child(text[i + node.get_level()]):
            node = node.get_child(text[i + node.get_level()])
            if node.leaf:
                return True

        if node is not root:
            i = i + node.get_level() - node.fail.get_level()
            node = node.fail
        else:
            i += 1

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aho-Corasick algorithm")
    parser.add_argument("--text", type=str, help="Text to search")
    parser.add_argument("--patterns", type=str, nargs="+", help="Patterns to search for")
    parser.add_argument("--path", type=str, help="Path to save tree image")

    args = parser.parse_args()

    if aho_corasick(args.text, args.patterns, args.path):
        print("Found")
    else:
        print("Not found")
