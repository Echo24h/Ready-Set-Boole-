def adder (a: int, b: int) -> int:
    while b != 0:
        carry = a & b
        a = a ^ b
        b = carry << 1
        
    return a

def multiplier(a: int, b: int) -> int:
    """
    Multiplies two integers using bitwise operations.
    
    Principle:
    - The multiplication is performed by adding 'a' to the result for each set bit in 'b'.
    - The value of 'a' is shifted left (a <<= 1) for each bit position in 'b'.
    - The value of 'b' is shifted right (b >>= 1) to process each bit.
    
    Example: 011 (3) * 101 (5) = 1111 (15)
    
    Step 1:
        if b (101 in binary) & 1:
            result = adder(result, a) -> result = 0 + 011 (3) = 011 (3)
        a <<= 1 -> a = 011 << 1 = 110 (6)
        b >>= 1 -> b = 101 >> 1 = 010 (2)
    
    Step 2:
        if b (010 in binary) & 1:
            -
        a <<= 1 -> a = 110 << 1 = 1100 (12)
        b >>= 1 -> b = 010 >> 1 = 001 (1)
    
    Step 3:
        if b (001 in binary) & 1:
            result = adder(result, a) -> result = 011 (3) + 1100 (12) = 1111 (15)
        a <<= 1 -> a = 1100 << 1 = 11000 (24)
        b >>= 1 -> b = 001 >> 1 = 000 (0)
    
    Final result: 1111 (15)
    """
    result = 0
    while b > 0:
        if b & 1: # Check if the least significant bit of b is set
            result = adder(result, a)
        a <<= 1
        b >>= 1
    return result


if __name__ == "__main__":

    test_cases = [
        (3, 5),   # 3 * 5 = 15
        (0, 10),  # 0 * 10 = 0
        (7, 0),   # 7 * 0 = 0
        (4, 4),   # 4 * 4 = 16
        (6, 7),   # 6 * 7 = 42
        (1, 1),   # 1 * 1 = 1
        (2, -3),  # 2 * -3 = -6
        (-2, -3), # -2 * -3 = 6
    ]

    for a, b in test_cases:
        result = multiplier(a, b)
        print(f"{a} * {b} = {result}")