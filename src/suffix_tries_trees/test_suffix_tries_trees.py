from ukkonnen import Tree

def test_tree():
    tree = Tree("ababc")

    assert tree.root.children["c"].is_terminal()