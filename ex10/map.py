def _interleave_bits_16(x: int) -> int:
    """Interleave the bits of a 16-bit integer with zeros.

    This produces a 32-bit integer where the original bits occupy the even
    bit positions (0, 2, 4, ...).
    """
    x &= 0xFFFF
    x = (x | (x << 8)) & 0x00FF00FF
    x = (x | (x << 4)) & 0x0F0F0F0F
    x = (x | (x << 2)) & 0x33333333
    x = (x | (x << 1)) & 0x55555555
    return x


def map(x: int, y: int) -> float:
    """Map a 2D coordinate pair to a unique value in [0, 1].

    The function is bijective for inputs in the range [0, 2^16 - 1]. It uses
    a Morton / Z-order curve by interleaving the bits of x and y to produce a
    32-bit code, then normalizes that code to the closed interval [0, 1].

    Args:
        x (int): X coordinate in [0, 65535].
        y (int): Y coordinate in [0, 65535].

    Returns:
        float: A unique value in [0, 1] representing the pair (x, y).
    """
    if not (0 <= x <= 0xFFFF) or not (0 <= y <= 0xFFFF):
        raise ValueError("Input coordinates must be in the range [0, 65535].")

    morton_x = _interleave_bits_16(x)
    morton_y = _interleave_bits_16(y) << 1
    morton_code = morton_x | morton_y

    return morton_code / 0xFFFFFFFF


if __name__ == "__main__":
    examples = [
        (0, 0),
        (65535, 65535),
        (65535, 0),
        (0, 65535),
        (12345, 54321),
    ]

    for x, y in examples:
        value = map(x, y)
        print(f"map({x}, {y}) = {value}")

    # Verify endpoints
    assert map(0, 0) == 0.0
    assert map(65535, 65535) == 1.0

