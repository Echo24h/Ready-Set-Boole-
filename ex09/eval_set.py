def eval_set(formula: str, sets: list[list[int]]) -> list[int]:
    """
    Evaluates a formula against a list of sets.

    Args:
        formula (str): The formula to evaluate.
        sets (list[list[int]]): A list of sets to evaluate the formula against.

    Returns:
        list[int]: A sorted list of integers representing the resulting set.
    """
    if not formula:
        raise ValueError("Formula cannot be empty.")

    valid_ops = set("!&|^>=")
    for char in formula:
        if not (char.isupper() or char in valid_ops):
            raise ValueError(f"Invalid character '{char}' in formula.")

    set_values = [set(item) for item in sets]
    universe = set().union(*set_values) if set_values else set()

    stack: list[set[int]] = []
    for char in formula:
        if char.isupper():
            index = ord(char) - ord('A')
            if index < 0 or index >= len(set_values):
                raise ValueError(f"Variable '{char}' is not defined by the provided sets.")
            stack.append(set_values[index])
        elif char == '!':
            if not stack:
                raise ValueError("Invalid formula: missing operand for '!'.")
            operand = stack.pop()
            stack.append(universe - operand)
        else:
            if len(stack) < 2:
                raise ValueError(f"Invalid formula: missing operands for '{char}'.")
            right = stack.pop()
            left = stack.pop()
            if char == '&':
                stack.append(left & right)
            elif char == '|':
                stack.append(left | right)
            elif char == '^':
                stack.append(left ^ right)
            elif char == '>':
                stack.append((universe - left) | right)
            elif char == '=':
                stack.append((left & right) | ((universe - left) & (universe - right)))
            else:
                raise ValueError(f"Unsupported operator '{char}'.")

    if len(stack) != 1:
        raise ValueError("Invalid formula: stack should contain exactly one result at the end.")

    return sorted(stack.pop())


if __name__ == "__main__":

    examples = [
        ("AB&", [[0, 1, 2], [0, 3, 4]]),
        ("AB&", [[0, 1, 2], [0, 1, 4]]),
        ("AB|", [[0, 1, 2], [3, 4, 5]]),
        ("AB|", [[0, 1, 2], [0, 1, 4]]),
        ("A!", [[0, 1, 2]]),
    ]

    for formula, sets in examples:
        result = eval_set(formula, sets)
        print(f"Formula: {formula}")
        print(f"Sets: {sets}")
        print(f"Result: {result}\n")
