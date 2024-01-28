#!/usr/bin/env python3

import numpy as np
from typing import List, Tuple

def knapsack(items: List[Tuple[int, int]], capacity: int):
    """
    Knapsack problem solver using dynamic programming.
    :param items: list of tuples (weight, value)
    :return: tuple (max_value, max_weight)
    """

    # Check if capacity is valid
    if capacity < 0:
        raise ValueError("Capacity must be positive")
    
    max_k = len(items)
    max_p = sum([p for _, p in items])

    # Create matrix
    S = np.zeros((max_k + 1, max_p + 1))

    for k in range(max_k + 1):
        for p in range(max_p + 1):
            if k == 0:
                if p == 0:
                    S[k, p] = 0
                else:
                    S[k, p] = np.inf
            else:
                p_k = items[k - 1][1]
                s_k = items[k - 1][0]

                if p - p_k >= 0 and \
                        S[k - 1, p - p_k] != np.inf and \
                        S[k - 1, p - p_k] + s_k <= capacity and \
                        S[k - 1, p - p_k] + s_k <= S[k - 1, p]:
                    S[k, p] = S[k - 1, p - p_k] + s_k
                else:
                    S[k, p] = S[k - 1, p]
    
    # Find max position that is smaller or equal to capacity
    p = max_p
    while S[max_k, p] > capacity:
        p -= 1
    
    return p, S[max_k, p]

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--items', "-i", help='items string, e.g. "3:1;4:2;2:3', default='3:1;4:2;2:3', required=False)
    parser.add_argument('--capacity', "-c", help='knapsack capacity', type=int, default=5, required=False)

    args = parser.parse_args()

    items = [(int(w), int(p)) for w, p in [i.split(':') for i in args.items.split(';')]]
    capacity = args.capacity

    max_value, weight = knapsack(items, capacity)

    print("Max value:", max_value)
    print("Weight:", weight)
