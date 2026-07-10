# Allowed operators for this exercise:

# &  : bitwise AND
#      Example:  6 & 3  ->  110 & 011 = 010 (2)

# |  : bitwise OR
#      Example:  6 | 3  ->  110 | 011 = 111 (7)

# ^  : bitwise XOR
#      Example:  6 ^ 3  ->  110 ^ 011 = 101 (5)

# << : left shift
#      Example:  3 << 1 ->  011 << 1 = 110 (6)

# >> : right shift
#      Example:  6 >> 1 ->  110 >> 1 = 011 (3)

# =  : assignment

# == : equal to

# != : not equal to

# <  : strictly less than

# >  : strictly greater than

# <= : less than or equal to

# >= : greater than or equal to

# ++ or += 1 : allowed ONLY to increment a loop index


def adder (a: int, b: int) -> int:
    """
    Adds two integers without using the + operator.

    Principle:
    - XOR (a ^ b) computes the sum without carries.
    - AND (a & b) identifies carry bits.
    - Carries are shifted left (carry << 1) to be added on the next iteration.
    - The process repeats until no carry remains (b == 0).

    Example: 0100 (4) + 1101 (13) = 10001 (17)

    Step 1:
        carry = 0100 & 1101 = 0100
        a     = 0100 ^ 1101 = 1001 (9)
        b     = 0100 << 1   = 1000 (8)

    Step 2:
        carry = 1001 & 1000 = 1000
        a     = 1001 ^ 1000 = 0001 (1)
        b     = 1000 << 1   = 10000 (16)

    Step 3:
        carry = 0001 & 10000 = 00000
        a     = 0001 ^ 10000 = 10001 (17)
        b     = 00000 << 1   = 00000 (0)

    Final result: 10001 (17)
    """
    while b != 0:
        carry = a & b
        a = a ^ b
        b = carry << 1
        
    return a


if __name__ == "__main__":

    tests = [
        (0, 0),             # 0 + 0 = 0
        (0, 5),             # 0 + 5 = 5
        (5, 0),             # 5 + 0 = 5
        (1, 1),             # 1 + 1 = 2
        (2, 3),             # 2 + 3 = 5
        (10, 15),           # 10 + 15 = 25
        (123456, 654321),   # 123456 + 654321 = 777777
        ((1 << 32) - 2, 1), # (2^32 - 2) + 1 = 2^32 - 1
    ]

    for a, b in tests:
        result = adder(a, b)
        print(f"adder({a}, {b}) = {result}")
