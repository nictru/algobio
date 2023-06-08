#!/usr/bin/env python3

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import pydot

@dataclass
class Node:
    

    
    def __init__(self, id: str = "root", parent: Tuple["Node", str] | None = None):
        self.parent = parent
        self.id: str = id

        self.fail: "Node" | None = None
        self.leaf: bool = False
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
    def build(patterns: List[str]) -> "Node":
        root: Node = Node()
        for pattern in patterns:
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

            node.leaf = True

        # Add fail links
        max_depth = max([len(pattern) for pattern in patterns]) + 1

        for length in range(1, max_depth):
            for node in root.get_children(length):
                if node.parent is None:
                    raise Exception("Node has no parent")
                
                parent, parent_char = node.parent

                w = parent.fail

                while w is not None and w is not root and w.children.get(parent_char, None) is None:
                    w = w.fail

                if w is not None and w.children.get(parent_char, None) is not None:
                    node.fail = w.children[parent_char]
                else:
                    node.fail = root

        return root

    def tree(self, path: str = "tree.png") -> None:
        graph = pydot.Dot(graph_type="digraph")

        for depth in range(self.get_max_depth() + 1):
            for node in self.get_children(depth):
                graph.add_node(pydot.Node(node.id, label=node.id))

                if node.fail is not None:
                    graph.add_edge(pydot.Edge(node.id, node.fail.id, style="dashed"))


                for char, child in node.children.items():
                    graph.add_edge(pydot.Edge(node.id, child.id, label=char))

        graph.write_png(path)

def aho_corasick(text: str, patterns: List[str], path: str | None = None) -> bool:
    root = Node.build(patterns)

    root.tree(path) if path is not None else root.tree()

    node: Node | None = root
    i = 0

    while i < len(text):
        while checked := node.children.get(text[i + node.get_level()]):
            node = checked
            if node.leaf:
                return True
            
        if node is None:
            raise Exception("Node is None")

        if node is not root:
            i = i + node.get_level() - node.fail.get_level()
            node = node.fail
        else:
            i += 1

    return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aho-Corasick algorithm")
    parser.add_argument("--text", default="aausau", type=str, help="Text to search")
    parser.add_argument("--patterns", default=["aal", "aas", "aus", "sau"], type=str, nargs="+", help="Patterns to search for")
    parser.add_argument("--path", type=str, help="Path to save tree image")

    args = parser.parse_args()

    if aho_corasick(args.text, args.patterns, args.path):
        print("Found")
    else:
        print("Not found")
