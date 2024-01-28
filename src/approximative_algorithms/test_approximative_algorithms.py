from knapsack import knapsack
import pytest

def test_knapsack():
    items = [(3, 1), (4, 2), (2, 3)]
    capacity = 5

    max_value, weight, items = knapsack(items, capacity)

    assert max_value == 4
    assert weight == 5
    assert items == {0, 2}

    with pytest.raises(ValueError):
        knapsack(items, -1)
