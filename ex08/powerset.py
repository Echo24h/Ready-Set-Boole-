
def powerset(set: list[int]) -> list[list[int]]:
    """
    Generate the powerset of a given list of integers.

    Args:
        set (list[int]): The input list of integers.

    Returns:
        list[list[int]]: A list of subsets representing the powerset.
    """
    result = []
    x = len(set)
    limit = 1 << x  # 2^x subsets
    for i in range(limit):
        subset = []
        for j in range(x):
            if (i & (1 << j)) > 0:
                subset.append(set[j])
        result.append(subset)
    return result


if __name__ == "__main__":
    A = [4, 5, 6]
    P = powerset(A)
    for subset in P:
        print(subset)
