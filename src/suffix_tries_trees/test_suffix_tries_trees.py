from ukkonnen import Tree


def test_tree():
    tree = Tree("ababc")

    assert "c" in [child.get_label(tree) for child in tree.root.children.values()]
