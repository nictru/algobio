#!/usr/bin/env python3


def log(msg: str = "", verbose: bool = False):
    if verbose:
        print(msg)


def z_boxes(pattern: str, verbose: bool = False):
    """
    Compute the Z-boxes for the Z-algorithm.
    """
    m = len(pattern)

    l = r = 0
    i = 1

    Z = [0] * m

    log(f"Initial values: l = {l}, r = {r}, i = {i}", verbose)

    for k in range(1, m):
        log(verbose=verbose)
        log(f"Iteration: k = {k}", verbose)

        if k > r:
            log(f"Case 1: k > r", verbose)
            i = k
            while i < m and pattern[i] == pattern[i - k]:
                log(f"Inner loop: i = {i}", verbose)
                i += 1

            if i >= m:
                log(f"Left inner loop: i = {i} >= m = {m}", verbose)
            else:
                log(
                    f"Left inner loop: pattern[i] = {pattern[i]} != pattern[i - k] = {pattern[i - k]}",
                    verbose,
                )

            log(f"Set Z[{k}] to {i - k}", verbose)
            Z[k] = i - k

            if Z[k] > 0:
                log(f"Since Z[{k}] > 0, set l to {k} and r to {i - 1}", verbose)
                l = k
                r = i - 1
        else:
            if Z[k - l] < r - k + 1:
                log(f"Case 2a: Z[k - l] < r - k + 1", verbose)
                log(f"Set Z[{k}] to Z[{k - l}] = {Z[k - l]}", verbose)
                Z[k] = Z[k - l]
            else:
                log(f"Case 2b: Z[k - l] >= r - k + 1", verbose)
                i = r + 1
                while i < m and pattern[i] == pattern[i - k]:
                    log(f"Inner loop: i = {i}", verbose)
                    i += 1

                if i >= m:
                    log(f"Left inner loop: i = {i} >= m = {m}", verbose)
                else:
                    log(
                        f"Left inner loop: pattern[i] = {pattern[i]} != pattern[i - k] = {pattern[i - k]}",
                        verbose,
                    )

                log(f"Set Z[{k}] to {i - k}", verbose)
                Z[k] = i - k

                if i - 1 > r:
                    log(f"Since i - 1 > r, set l to {k} and r to {i - 1}", verbose)
                    l = k
                    r = i - 1

    return Z


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Z-boxes algorithm")
    parser.add_argument("--pattern", type=str, help="Pattern to search for")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    verbose = args.verbose

    print(z_boxes(args.pattern, args.verbose))
