#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict, Tuple
import pydot

@dataclass
class Node:
    def __init__(self, id: str = "root", parent: Tuple["Node", str] | None = None):
        self.parent = parent
        self.id: str = id

        self.fail: "Node" | None = None
        self.leaf: bool = False
        self.hit: bool = False
        self.hit_link: "Node" | None = None
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
            node.hit = True
            node.hit_link = node

        # Add fail links
        max_depth = max([len(pattern) for pattern in patterns])

        for length in range(1, max_depth):
            for node in root.get_children(length):
                if node.parent is None:
                    raise Exception("Node has no parent")
                
                # Find out how this node can be reached
                parent, parent_char = node.parent

                # Find the highest-level node that is in a failure-linkage chain starting at the parent
                # and has a child with the desired character
                w = parent.fail
                while w is not None and w is not root and w.children.get(parent_char, None) is None:
                    w = w.fail

                # If such a node exists, set the failure link to the child of that node with the desired character
                if w is not None and w.children.get(parent_char, None) is not None:
                    node.fail = w.children[parent_char]
                
                # Otherwise, set the failure link to the root
                else:
                    node.fail = root

                # Extension: This way, real partial words can be found as well
                if node.fail.hit:
                    node.hit = True
                    node.hit_link = node.fail.hit_link

        return root

    def tree(self, path: str = "tree.png") -> None:
        graph = pydot.Dot(graph_type="digraph")

        for depth in range(self.get_max_depth() + 1):
            for node in self.get_children(depth):
                if node.hit:
                    if node.leaf:
                        graph.add_node(pydot.Node(node.id, style="filled", fillcolor="green"))
                    else:
                        graph.add_node(pydot.Node(node.id, style="filled", fillcolor="red"))
                else:
                    graph.add_node(pydot.Node(node.id))

                if node.fail is not None:
                    graph.add_edge(pydot.Edge(node.id, node.fail.id, style="dashed"))

                if node.hit_link is not None and node is not node.hit_link:
                    graph.add_edge(pydot.Edge(node.id, node.hit_link.id, style="dotted"))


                for char, child in node.children.items():
                    graph.add_edge(pydot.Edge(node.id, child.id, label=char))

        graph.write_png(path)

def aho_corasick_binary(text: str, patterns: List[str], path: str | None = None) -> bool:
    root = Node.build(patterns)

    root.tree(path) if path is not None else root.tree()

    node: Node | None = root
    i = 0

    while i < len(text):
        while checked := node.children.get(text[i + node.get_level()]):
            node = checked
            if node.hit:
                return True
            
        if node is None:
            raise Exception("Node is None")

        if node is not root and node.fail is not None:
            i = i + node.get_level() - node.fail.get_level()
            node = node.fail
        else:
            i += 1

    return False

def aho_corasick_patterns(text: str, patterns: List[str], path: str | None = None) -> List[str]:
    root = Node.build(patterns)

    root.tree(path) if path is not None else root.tree()

    node: Node = root

    result: List[str] = []

    for letter in text:
        # Find first node with this letter, following fail links if necessary
        while node.children.get(letter, None) is None and node is not root:
            if node.fail is None:
                raise Exception("Node has no fail link")

            node = node.fail

        # Investigate the corresponding child
        node = node.children[letter]

        if node.hit:
            result.append(node.id)
    

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Aho-Corasick algorithm")
    parser.add_argument("--text", default="cbcabcbca", type=str, help="Text to search")
    parser.add_argument("--patterns", default=["abcbca", "bcbcb", "c", "cbc", "cbcc"], type=str, nargs="+", help="Patterns to search for")
    parser.add_argument("--path", type=str, help="Path to save tree image")

    args = parser.parse_args()

    if aho_corasick_binary(args.text, args.patterns, args.path):
        print("Found")
    else:
        print("Not found")

    print(aho_corasick_patterns(args.text, args.patterns, args.path))
