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


# -------------------------------------------------------------------------------------- #
# The code above this line is unchanged from the previous exercise. The code below is new.
# -------------------------------------------------------------------------------------- #


def distribute_or(a: tuple, b: tuple) -> tuple:
    """
    Distribute an OR over an AND, so that '|' always ends up "below" '&'.
 
    Rule used (both directions of the distributive law):
        a | (b & c)  ==  (a | b) & (a | c)
        (a & b) | c  ==  (a | c) & (b | c)
 
    `a` and `b` are assumed to already be in CNF (i.e. any 'and'/'or' inside
    them already respects the CNF shape: 'or' never contains an 'and').
 
    Example:
        distribute_or(('var', 'A'), ('and', ('var', 'B'), ('var', 'C')))
        -> ('and', ('or', ('var', 'A'), ('var', 'B')),
                    ('or', ('var', 'A'), ('var', 'C')))
    """
    if a[0] == 'and':
        return ('and', distribute_or(a[1], b), distribute_or(a[2], b))
 
    if b[0] == 'and':
        return ('and', distribute_or(a, b[1]), distribute_or(a, b[2]))
 
    return ('or', a, b)
 
 
def to_cnf_tree(node: tuple) -> tuple:
    """
    Turn a NNF tree (only var / not / and / or, negations on variables only)
    into an equivalent tree in Conjunctive Normal Form: a conjunction of
    disjunctions of (possibly negated) variables.
 
    'and' nodes are kept as-is (recursively converted).
    'or' nodes are converted by first converting both sides to CNF, then
    distributing '|' over any remaining '&' with distribute_or.
    """
    kind = node[0]
 
    if kind in ('var', 'not'):
        return node
 
    if kind == 'and':
        return ('and', to_cnf_tree(node[1]), to_cnf_tree(node[2]))
 
    if kind == 'or':
        left = to_cnf_tree(node[1])
        right = to_cnf_tree(node[2])
        return distribute_or(left, right)
 
    raise ValueError(f"unexpected node kind in NNF tree: {kind}")


def flatten_associative(node: tuple, kind: str) -> list:
    """
    Collect the operands of a chain of the same associative operator
    ('and' with 'and', or 'or' with 'or') into a flat list, in the order
    they originally appear (left to right).
 
    Descends only through nodes of the given `kind`; anything else
    (a variable, a negation, or a node of the *other* kind) is treated as
    a single opaque operand and stops the recursion on that branch.
 
    Example:
        flatten_associative(('and', ('and', ('var','A'), ('var','B')), ('var','C')), 'and')
        -> [('var', 'A'), ('var', 'B'), ('var', 'C')]
    """
    if node[0] == kind:
        return flatten_associative(node[1], kind) + flatten_associative(node[2], kind)
    return [node]
 
 
def rebuild_right_associative(kind: str, operands: list) -> tuple:
    """
    Rebuild a right-associative tree of the given `kind` ('and' or 'or')
    from a flat list of operands, preserving their left-to-right order.
 
    Example:
        rebuild_right_associative('and', [A, B, C, D])
        -> ('and', A, ('and', B, ('and', C, D)))
    """
    if len(operands) == 1:
        return operands[0]
    return (kind, operands[0], rebuild_right_associative(kind, operands[1:]))


def normalize(node: tuple) -> tuple:
    """
    Canonicalize a var/not/and/or tree: every maximal chain of the same
    operator ('and'...'and' or 'or'...'or'), regardless of how it was
    nested originally, is flattened and rebuilt as a right-associative
    chain. This gives a single canonical shape among the many equivalent
    trees, e.g. turning ((A|B)|C)|D into A|(B|(C|D)), which serializes as
    "ABCD|||" instead of "AB|C|D|".
    """
    kind = node[0]
 
    if kind in ('var', 'not'):
        return node
 
    if kind in ('and', 'or'):
        operands = [normalize(operand) for operand in flatten_associative(node, kind)]
        return rebuild_right_associative(kind, operands)
 
    raise ValueError(f"unexpected node kind: {kind}")

 
def conjunctive_normal_form(formula: str) -> str:
    """
    Convert a RPN formula into its conjunctive normal form (CNF).
 
    Example:
        For the formula "AB&C&D&", the CNF will be "ABCD&&&"
    """
    # 1. Parse and simplify down to NNF (only var / not / and / or, negations pushed onto the variables).
    nodes = parse(formula)
    if nodes is None:
        raise ValueError("Invalid formula")
    simplified = eliminate(nodes)
    nnf = push_negation(simplified)
 
    # 2. Distribute '|' over '&' until every '|' is below every '&'.
    cnf_tree = to_cnf_tree(nnf)

    # 3. Canonicalize associative chains into a single, predictable shape.
    cnf_tree = normalize(cnf_tree)

    # 4. Convert the tree back into a RPN formula.
    return to_rpn(cnf_tree)


if __name__ == "__main__":
    test_cases = [
        "AB&!",     # expected result: A!B!|
        "AB|!",     # expected result: A!B!&
        "AB|C&",    # expected result: AB|C&
        "AB|C|D|",  # expected result: ABCD|||
        "AB&C&D&",  # expected result: ABCD&&&
        "AB&!C!|",  # expected result: A!B!C!||
        "AB|!C!&",  # expected result: A!B!C!&&
        "ABCD&&&",  # expected result: ABCD&&&
    ]

    for formula in test_cases:
        cnf = conjunctive_normal_form(formula)
        print(f"CNF of {formula} is {cnf}")
