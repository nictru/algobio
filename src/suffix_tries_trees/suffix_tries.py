#!/usr/bin/env python3

from dataclasses import dataclass
from typing import List, Dict
import pydot

@dataclass
class Node:
    TERMINAL = "$"

    def __init__(self, id: str = "root", parent = None):
        self.parent: "Node" | None = parent
        self.id: str = id

        self.terminal: bool = False
        self.suffix_link: "Node" | None = None
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
            return self.parent.get_level() + 1
        
    def get_label(self) -> str:
        if self.parent is None:
            return "(virtual root)"
        elif self.parent.parent is None:
            return "(epsilon)"
        else:
            edges = [edge for edge in self.parent.children.keys() if self.parent.children[edge] == self]
            parent_label = self.parent.get_label()
            return (parent_label if parent_label != "(epsilon)" else "") + (edges[0] if len(edges) == 1 else f"({'|'.join(edges)})")

    def __hash__(self) -> int:
        return hash(self.id)

    @staticmethod
    def build(pattern: str) -> "Node":
        if Node.TERMINAL in pattern:
            raise ValueError("Pattern cannot contain " + Node.TERMINAL + " symbol")

        pattern += Node.TERMINAL

        alphabet = set(pattern)

        meta_root = Node(id="meta")
        root = Node(parent=meta_root)

        root.suffix_link = meta_root

        for letter in alphabet:
            meta_root.children[letter] = root

        longest_suffix = root

        n = len(pattern)

        for i in range(n):
            print("i:", i)
            curr_node = longest_suffix
            print("curr_node:", curr_node.id)
            letter = pattern[i]
            print("letter:", letter)

            while not (letter in curr_node.children):
                new_node = Node(id=curr_node.id + letter, parent=curr_node)
                print("new_node:", new_node.id)
                curr_node.children[letter] = new_node

                if letter == Node.TERMINAL:
                    new_node.terminal = True

                if i == n - 1:
                    new_node.terminal = True

                if curr_node is longest_suffix:
                    longest_suffix = new_node
                else:
                    prev_node.suffix_link = new_node
                
                prev_node = new_node
                assert curr_node.suffix_link is not None
                curr_node = curr_node.suffix_link
                
            prev_node.suffix_link = curr_node.children[letter]

        return meta_root

    def save(self, path: str = "trie.png") -> None:
        graph = pydot.Dot(graph_type="digraph", size="30, 30")

        for depth in range(self.get_max_depth() + 1):
            for node in set(self.get_children(depth)):
                if node.terminal:
                    graph.add_node(pydot.Node(node.id, label=node.get_label(), shape="double"))
                else:
                    graph.add_node(pydot.Node(node.id, label=node.get_label()))

                if node.suffix_link is not None:
                    graph.add_edge(pydot.Edge(node.id, node.suffix_link.id, style="dashed"))

                for investigated in set(node.children.values()):
                    letters = [letter for letter, child in node.children.items() if child is investigated]
                    letters.sort()

                    graph.add_edge(pydot.Edge(node.id, investigated.id, label=", ".join(letters)))

        graph.write_png(path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Suffix trie builder")
    parser.add_argument("-w", "--word", default="abbaba", type=str, help="Word to build suffix trie for")
    parser.add_argument("-o", "--output", type=str, help="Output file name", default="trie.png")

    args = parser.parse_args()

    print(args.word)

    root = Node.build(args.word)

    root.save(args.output)

    print("Output saved to", args.output)