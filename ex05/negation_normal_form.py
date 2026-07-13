def parse(formula: str) -> tuple:   
    """
    Parse a RPN formula into a tree of nodes. Return None if the formula is invalid.

    A node is represented as a tuple:
    - ('var', 'A') for a variable A
    - ('not', node) for negation
    - ('and', left, right) for conjunction
    - ('or', left, right) for disjunction
    - ('xor', left, right) for exclusive OR
    - ('imply', left, right) for material condition
    - ('equiv', left, right) for logical equivalence
    
    Example: 
        For the formula "AB&!", the returned tree will be:
        ('not', ('and', ('var', 'A'), ('var', 'B')))
    """
    stack = []
 
    for c in formula:
        if c.isalpha() and c.isupper():
            stack.append(('var', c))
        elif c == '!':
            if not stack:
                return None
            a = stack.pop()
            stack.append(('not', a))
        elif c in '&|^>=':
            if len(stack) < 2:
                return None
            # RPN pushes `a` then `b`, so the second pop is `a`.
            b = stack.pop()
            a = stack.pop()
            kind = {'&': 'and', '|': 'or', '^': 'xor',
                    '>': 'imply', '=': 'equiv'}[c]
            stack.append((kind, a, b))
        else:
            return None  # unknown symbol -> invalid formula
 
    if len(stack) == 1:
        return stack[0]
    return None


def eliminate(node: tuple) -> tuple:
    """
    Eliminate '> (imply)', '= (equiv)' and '^ (xor)', keeping only var / not / and / or

    Example: 
        For the tree "('imply', ('var', 'A'), ('var', 'B'))", the tree will be transformed into:
        ('or', ('not', ('var', 'A')), ('var', 'B'))
    """
    kind = node[0]
 
    if kind == 'var':
        return node
 
    if kind == 'not':
        return ('not', eliminate(node[1]))
 
    if kind == 'and':
        return ('and', eliminate(node[1]), eliminate(node[2]))
 
    if kind == 'or':
        return ('or', eliminate(node[1]), eliminate(node[2]))
 
    if kind == 'imply':
        # a > b  ==  !a | b
        a = eliminate(node[1])
        b = eliminate(node[2])
        return ('or', ('not', a), b)
 
    if kind == 'xor':
        # a ^ b  ==  (a & !b) | (!a & b)
        a = eliminate(node[1])
        b = eliminate(node[2])
        left = ('and', a, ('not', b))
        right = ('and', ('not', a), b)
        return ('or', left, right)
 
    if kind == 'equiv':
        # a = b  ==  (a & b) | (!a & !b)
        a = eliminate(node[1])
        b = eliminate(node[2])
        left = ('and', a, b)
        right = ('and', ('not', a), ('not', b))
        return ('or', left, right)
 
    raise ValueError(f"unknown node kind: {kind}")


def push_negation(node: tuple, negate: bool = False) -> tuple:
    """
    Push negation down the tree, so that negations only apply to variables.

    Example:
        For the tree "('not', ('and', ('var', 'A'), ('var', 'B')))", the tree will be transformed into:
        ('or', ('not', ('var', 'A')), ('not', ('var', 'B')))
    """
    kind = node[0]
 
    if kind == 'var':
        return ('not', node) if negate else node
 
    if kind == 'not':
        return push_negation(node[1], not negate)
 
    if kind == 'and':
        a, b = node[1], node[2]
        if negate:
            # !(a & b) == !a | !b
            return ('or', push_negation(a, True), push_negation(b, True))
        return ('and', push_negation(a, False), push_negation(b, False))
 
    if kind == 'or':
        a, b = node[1], node[2]
        if negate:
            # !(a | b) == !a & !b
            return ('and', push_negation(a, True), push_negation(b, True))
        return ('or', push_negation(a, False), push_negation(b, False))
 
    raise ValueError(f"unexpected node kind in NNF output: {kind}")


def to_rpn(node: tuple) -> str:
    """
    Convert a tree of nodes back into a RPN formula.

    Example:
        For the tree "('or', ('not', ('var', 'A')), ('not', ('var', 'B')))", the RPN formula will be:
        "A!B!|"
    """
    kind = node[0]
 
    if kind == 'var':
        return node[1]
    if kind == 'not':
        return to_rpn(node[1]) + '!'
    if kind == 'and':
        return to_rpn(node[1]) + to_rpn(node[2]) + '&'
    if kind == 'or':
        return to_rpn(node[1]) + to_rpn(node[2]) + '|'
 
    raise ValueError(f"unexpected node kind in NNF output: {kind}")


def negation_normal_form(formula: str) -> str:
    """
    Convert a RPN formula into its negation normal form (NNF).

    Example:
        For the formula "AB&!", the NNF will be "A!B!|"
    """
    # 1. Parse the formula into a tree of nodes
    # Example: "AB&!" -> ('not', ('and', ('var', 'A'), ('var', 'B')))
    nodes = parse(formula)
    if nodes is None:
        raise ValueError("Invalid formula")
    # 2. Eliminate 'imply', 'equiv', and 'xor' from the tree
    # Example: ('imply', ('var', 'A'), ('var', 'B')) -> ('or', ('not', ('var', 'A')), ('var', 'B'))
    simplified = eliminate(nodes)
    # 3. Push negations down the tree, so that negations only apply to variables
    # Example: ('not', ('and', ('var', 'A'), ('var', 'B'))) -> ('or', ('not', ('var', 'A')), ('not', ('var', 'B')))
    nnf = push_negation(simplified)
    # 4. Convert the tree back into a RPN formula
    # Example: ('or', ('not', ('var', 'A')), ('not', ('var', 'B'))) -> "A!B!|"
    return to_rpn(nnf)


if __name__ == "__main__":
    test_cases = [
        "AB&!",     # expected result: A!B!|
        "AB|!",     # expected result: A!B!&
        "AB>",      # expected result: A!B|
        "AB=",      # expected result: AB&A!B!&|
        "AB|C&!",   # expected result: A!B!&C!|
        "A!B!|"     # expected result: A!B!|
    ]

    for formula in test_cases:
        nnf = negation_normal_form(formula)
        print(f"NNF of {formula} is {nnf}")
