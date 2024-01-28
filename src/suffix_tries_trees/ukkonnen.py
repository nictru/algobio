#!/usr/bin/env python3

from typing import List, Dict, Tuple
from dataclasses import dataclass
import pydot
import random

MAX_INT = 2**32 - 1


class Node:
    index = 0

    def __init__(self, parent=None):
        self.parent: "Node" | None = parent
        self.id: int = Node.index
        Node.index += 1

        self.suffix_link: "Node" | None = None
        self.children: Dict[Reference | str, "Node"] = {}

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

    def get_edge_with_prefix(
        self, prefix: str, tree: "Tree"
    ) -> "Reference | str | None":
        for edge in self.children.keys():
            if tree.resolve(edge).startswith(prefix):
                return edge
        return None

    def get_level(self):
        if self.parent is None:
            return 0
        else:
            return self.parent.get_level() + 1

    def get_label(self, tree: "Tree") -> str:
        if self.parent is None:
            return "(virtual root)"
        elif self.parent.parent is None:
            return "(epsilon)"
        else:
            edges = [
                tree.resolve(edge)
                for edge in self.parent.children.keys()
                if self.parent.children[edge] == self
            ]
            parent_label = self.parent.get_label(tree)
            return (parent_label if parent_label != "(epsilon)" else "") + (
                edges[0] if len(edges) == 1 else f"({'|'.join(edges)})"
            )

    def is_terminal(self) -> bool:
        return len(self.children) == 0

    def __hash__(self) -> int:
        return hash(self.id)

    def to_string(self, tree: "Tree") -> str:
        return f"{self.get_label(tree)}"


@dataclass(eq=True, frozen=True)
class Reference:
    start: int
    end: int

    def __str__(self) -> str:
        return f"({self.start}, {self.end if self.end < MAX_INT else 'inf'})"


class Tree:
    def log(self, message: str = "") -> None:
        if self.verbose:
            print(message)

    def __init__(self, word: str, verbose: bool = False) -> None:
        self.verbose = verbose
        self.word = word

        n = len(word)

        self.log("[SuffixTree]")
        self.log(f"Word: {word}")
        self.log(f"Length: {n}")

        self.alphabet = set(word)

        # Init meta and root nodes

        v_root = Node()
        self.root = Node(parent=v_root)

        self.root.suffix_link = v_root
        v_root.children = {letter: self.root for letter in self.alphabet}

        # Init first node

        v = Node(parent=self.root)
        self.root.children[Reference(1, MAX_INT)] = v

        s = self.root
        k = 2

        self.save("step_1.png")
        for i in range(2, n + 1):
            s, k = self.update(s, Reference(k, i - 1), i)
            self.save(f"step_{i}.png")

    def resolve(self, reference: Reference | str) -> str:
        if isinstance(reference, Reference):
            return self.word[reference.start - 1 : reference.end]
        else:
            return reference

    def test_and_split(
        self, node: Node, reference: Reference, x: str
    ) -> Tuple[bool, Node]:
        self.log()
        self.log(f"\t[Test and split]")
        self.log(f"\tNode: {node.to_string(self)}")
        self.log(f"\tReference: {reference}")
        self.log(f"\tx: {x}")

        if reference.end - reference.start + 1 == 0:
            if any([self.resolve(edge).startswith(x) for edge in node.children.keys()]):
                self.log("\tReference is empty, but there is an edge starting with x")
                self.log(f"\tReturning True and {node.to_string(self)}")
                return True, node
            else:
                self.log("\tReference is empty, and there is no edge starting with x")
                self.log(f"\tReturning False and {node.to_string(self)}")
                return False, node

        else:
            edge = node.get_edge_with_prefix(self.word[reference.start - 1], self)
            if edge is None:
                raise Exception("Edge not found")
            w = self.resolve(edge)

            target = node.children[edge]  # s'

            self.log("\tW: " + w)

            if x == w[reference.end - reference.start + 1]:
                self.log("\tx is the same as the referenced letter of the edge")
                self.log(f"\tWe return True and {node.to_string(self)}")
                return True, node
            else:
                self.log(
                    "\tx is not the same as the referenced letter of the edge, so we split the edge"
                )
                r = Node(parent=node)

                if not isinstance(edge, Reference):
                    raise Exception("Edge is not a reference")

                self.log(
                    f"\tOriginal edge(s) starting at {node.to_string(self)}: {node.children.keys()}"
                )
                self.log(f"\tRemoving edge {edge}")
                node.children.pop(edge)

                separator = edge.start + reference.end - reference.start
                new_reference_1 = Reference(edge.start, separator)
                self.log(f"\tAdding edge {new_reference_1} to {node.to_string(self)}")
                node.children[new_reference_1] = r

                new_reference_2 = Reference(separator + 1, edge.end)
                self.log(f"\tAdding edge {new_reference_2} to {r.to_string(self)}")
                r.children[new_reference_2] = target

                target.parent = r

                self.log(f"\tWe return False and {r.to_string(self)}")
                return False, r

    def canonize(self, node: Node, reference: Reference):
        self.log()
        self.log("\t[Canonize]")
        self.log(f"\tNode: {node.to_string(self)}")
        self.log(f"\tReference: {reference}")

        while reference.end - reference.start + 1 > 0:
            first_reference_letter = self.word[reference.start - 1]

            edge = node.get_edge_with_prefix(first_reference_letter, self)

            if edge is None:
                print(node.to_string(self))
                print({child: self.resolve(child) for child in node.children.keys()})
                print(first_reference_letter)
                raise Exception("Edge is None")

            w = self.resolve(edge)
            child = node.children[edge]  # s'
            w_length = len(w)

            if w_length > (reference.end - reference.start + 1) or child.is_terminal():
                break

            reference = Reference(reference.start + w_length, reference.end)
            node = child

        self.log(f"\tReturning {node.to_string(self)} and {reference.start}")
        return node, reference.start

    def update(self, s: Node, reference: Reference, i: int) -> Tuple[Node, int]:
        self.log()
        self.log("[Update]")
        self.log(f"i: {i}, ti: {self.word[i-1]}")
        self.log(f"Reference: {reference}")
        self.log(f"Node: {s.to_string(self)}")
        old_r = self.root
        s, k = self.canonize(s, reference)

        done, r = self.test_and_split(s, Reference(k, reference.end), self.word[i - 1])

        while not done:
            self.log()
            self.log(f"Not done, creating new child for {r.to_string(self)}")
            m = Node(parent=r)
            r.children[Reference(i, MAX_INT)] = m

            if old_r is not self.root:
                old_r.suffix_link = r

            old_r = r

            if not s.suffix_link:
                raise Exception("Suffix link is not set")
            self.log(
                f"Following suffix link of {s.to_string(self)} to {s.suffix_link.to_string(self)}"
            )
            s, k = self.canonize(s.suffix_link, Reference(k, reference.end))
            done, r = self.test_and_split(
                s, Reference(k, reference.end), self.word[i - 1]
            )

        if old_r is not self.root:
            self.log(
                f"Setting suffix link of {old_r.to_string(self)} to {r.to_string(self)}"
            )
            old_r.suffix_link = r

        self.log(f"Returning {s.to_string(self)} and {k}")

        return s, k

    def save(self, filename: str) -> None:
        graph = pydot.Dot(graph_type="digraph")

        graph.add_node(pydot.Node("0", label="virtual_root"))

        def add_node(node: Node) -> None:
            graph.add_node(pydot.Node(str(node.id), label=node.get_label(self)))

            if node.suffix_link:
                graph.add_edge(
                    pydot.Edge(str(node.id), str(node.suffix_link.id), style="dashed")
                )

            for edge, child in node.children.items():
                graph.add_edge(
                    pydot.Edge(
                        str(node.id),
                        str(child.id),
                        label=str(edge) + "\n" + str(self.resolve(edge)),
                    )
                )
                add_node(child)

        add_node(self.root)

        graph.write_png(filename)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Suffix tree construction")
    parser.add_argument(
        "-w",
        "--word",
        default="caccacaccc",
        type=str,
        help="Word to build suffix tree for",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Provide step-by-step output"
    )
    parser.add_argument(
        "-o", "--output", default="tree.png", type=str, help="Output file name"
    )
    args = parser.parse_args()

    tree = Tree(args.word, True)
    tree.save(args.output)
