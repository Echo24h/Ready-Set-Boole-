def gray_code(n: int) -> int:
    """
    Generates the n-th Gray code number.

    Definition:
    - Gray code is a binary numeral system where two successive values differ in only one bit.
        000 in binary is 0 in Gray code (0 in decimal)
        001 in binary is 1 in Gray code (1 in decimal) 
        011 in binary is 2 in Gray code (3 in decimal) 
        010 in binary is 3 in Gray code (2 in decimal)
        110 in binary is 4 in Gray code (6 in decimal)
        111 in binary is 5 in Gray code (7 in decimal)
        101 in binary is 6 in Gray code (5 in decimal)
        100 in binary is 7 in Gray code (4 in decimal)

    Why Gray Code?
    - Gray code is used in digital systems to prevent errors during the transition between two successive values
    - It is particularly useful in applications like rotary encoders, where a single-bit change reduces the chance of misinterpretation during state changes.

    Principle:
    - The n-th Gray code can be computed using the formula: G(n) = n ^ (n >> 1)
    - This means that the Gray code is obtained by performing a bitwise XOR between n and n shifted right by one position.

    Example: For n = 3
        Binary representation of 3: 011
        Shifted right by 1: 001
        XOR operation: 011 ^ 001 = 010 (which is the Gray code for 3)

    Final result: 010 (2 in decimal)
    """
    gray = n ^ (n >> 1)
    return gray


if __name__ == "__main__":
    test_cases = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    for n in test_cases:
        gray = gray_code(n)
        print(f"Gray code for {n} is {gray} (binary: {gray:04b})")