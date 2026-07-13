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
                stack.append(left != right) # XOR
            elif char == '>':
                stack.append(not left or right) # Material condition
            elif char == '=':
                stack.append(left == right)  # Equivalence
    if len(stack) != 1:
        raise ValueError("Invalid formula: stack should contain exactly one result at the end.")
    return stack.pop()


def sat(formula: str) -> bool:
    """
    Determines if a given formula is satisfiable.

    A formula is satisfiable if there exists at least one assignment of truth values
    to its variables that makes the formula evaluate to true.

    Example:
        For the formula "AB&C|", the function will return True, since there exists
        an assignment (A=True, B=False, C=True) that makes the formula true.
    """
    if not formula:
        raise ValueError("Formula cannot be empty.")

    if any(char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ!&|^>=" for char in formula):
        raise ValueError("Formula contains invalid characters. Only A-Z and !&|^>= are allowed.")

    # Generate all possible combinations of truth values for the variables in the formula
    variables = sorted(set(filter(str.isalpha, formula)))
    num_vars = len(variables)

    num_combinations = 1 << num_vars # 2 ** num_vars
    
    for combination in range(num_combinations):
        # Turn the number "combination" into a sequence of bits.
        # Example: for 4 variables, combination 5 (0101 in binary) means A = 0, B = 1, C = 0, D = 1
        values = []
        for position in range(num_vars - 1, -1, -1):
            bit = (combination >> position) & 1
            values.append(bit)

        # Map variable names to their corresponding truth values
        # Example: if variables = ['A', 'B'] and values = [1, 0], then variable_values = {'A': 1, 'B': 0}
        variable_values = {}
        for variable, value in zip(variables, values):
            variable_values[variable] = value

        # Replace variables in the formula with their truth values (0 or 1)
        # Example: if formula = "AB&C|" and variable_values = {'A': 1, 'B': 0, 'C': 1}, then substituted_formula = "10&1|"
        substituted_formula = ""
        for char in formula:
            if char in variable_values:
                substituted_formula += str(variable_values[char])
            else:
                substituted_formula += char

        # Evaluate the formula using eval_formula function
        result = eval_formula(substituted_formula)
        if result:
            return True  # Found a satisfying assignment

    return False  # No satisfying assignment found


if __name__ == "__main__":
    test_cases = [
        "AB&C|",  # expected result: True
        "AB&!",   # expected result: True
        "AB|!",   # expected result: True
        "AB>",    # expected result: True
        "AB=",    # expected result: True
        "AB|C&!", # expected result: True
        "A!B!|",  # expected result: True
        "A!B!&",  # expected result: True
        "A!B!^",  # expected result: True
        "AB|",    # expected result: True
        "AB&",    # expected result: True
        "AA!&",    # expected result: False
        "AA^",    # expected result: False
    ]
    for formula in test_cases:
        result = sat(formula)
        print(f"Result of '{formula}' is {result}")
