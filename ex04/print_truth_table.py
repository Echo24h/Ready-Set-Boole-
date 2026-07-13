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


def print_truth_table(formula: str) -> None:
    """
    Prints the truth table for a given boolean formula in Reverse Polish Notation (RPN).

    Each character represents a logical symbol.
    Allowed characters:

    +---------+----------------------+-------------------------------------------+
    | Symbol  | Mathematical equiv. | Description                                |
    +---------+----------------------+-------------------------------------------+
    | A..Z    | A..Z                | distinct variables (unknown truth values)  |
    | !       | ¬                   | negation                                   |
    | &       | ∧                   | conjunction (AND)                          |
    | |       | ∨                   | disjunction (OR)                           |
    | ^       | ⊕                   | exclusive OR (XOR)                         |
    | >       | ⇒                   | material condition                         |
    | =       | ⇔                   | logical equivalence                        |
    +---------+----------------------+-------------------------------------------+

    Example: For the formula "AB&C|", the truth table will be printed as follows:
    | A | B | C | = |
    |---|---|---|---|
    | 0 | 0 | 0 | 0 |
    | 0 | 0 | 1 | 1 |
    | 0 | 1 | 0 | 0 |
    | 0 | 1 | 1 | 1 |
    | 1 | 0 | 0 | 0 |
    | 1 | 0 | 1 | 1 |
    | 1 | 1 | 0 | 1 |
    | 1 | 1 | 1 | 1 |
    """
    # Extract unique variables from the formula
    variables = []
    for char in formula:
        if char.isalpha() and char not in variables:
            variables.append(char)
    variables.sort()  # Sort variables for consistent order

    num_vars = len(variables)

    # Print header
    header = "| " + " | ".join(variables) + " | = |"
    print(header)
    print("|" + "---|" * num_vars + "---|")

    # Try every possible combination of True/False
    num_combinations = 2 ** num_vars

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

        # Print the current combination and its result
        print("| " + " | ".join(str(v) for v in values) + f" | {int(result)} |")


if __name__ == "__main__":

    formula = "AB&C|"

    print_truth_table(formula)
