def eval_formula(formula: str) -> bool:
    """
    Evaluates a mathematical formula represented as a string.

    Each character represents a logical symbol.
    The input contains only the following characters:

    +---------+----------------------+---------------------------+
    | Symbol  | Mathematical equiv. | Description               |
    +---------+----------------------+---------------------------+
    |   0     |        ⊥            | false                     |
    |   1     |        ⊤            | true                      |
    |   !     |        ¬            | negation                  |
    |   &     |        ∧            | conjunction (AND)         |
    |   |     |        ∨            | disjunction (OR)          |
    |   ^     |        ⊕            | exclusive OR (XOR)        |
    |   >     |        ⇒            | material condition        |
    |   =     |        ⇔            | logical equivalence       |
    +---------+----------------------+---------------------------+

    The formula is evaluated using a stack:

    - Operands are pushed onto the stack.
    - Operators pop the top operands, compute a result,
      then push the result back.

    Example: "10&"

        1. Push '1'
        2. Push '0'
        3. '&' operator:
            - Pop 0 and 1
            - Compute 1 AND 0 = false
            - Push false

    Final result: false
    """
    if not formula:
        raise ValueError("Formula cannot be empty.")

    for char in formula:
        if char not in "01!&|^>=":
            raise ValueError(f"Invalid character '{char}' in formula.")
        
    stack = []
    for char in formula:
        if char == '0':
            stack.append(False)
        elif char == '1':
            stack.append(True)
        elif char == '!':
            operand = stack.pop()
            stack.append(not operand) # Negation
        elif char in '&|^>=':
            right = stack.pop()
            left = stack.pop()
            if char == '&':
                stack.append(left and right) # AND
            elif char == '|':
                stack.append(left or right) # OR
            elif char == '^':
                stack.append(left != right)  # XOR
            elif char == '>':
                stack.append(not left or right) # Material implication
            elif char == '=':
                stack.append(left == right)  # Equivalence

    if len(stack) != 1:
        raise ValueError("Invalid formula: stack should contain exactly one result at the end.")

    return stack.pop()


if __name__ == "__main__":
    test_cases = [
        "10&",
        "10|",
        "10|1&",
        "101|&",
        "11>",
        "10=",
        "1011||="
    ]

    for formula in test_cases:
        result = eval_formula(formula)
        print(f"Result of '{formula}' is {result}")
