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


def _compact_bits_32(x: int) -> int:
    """Compact the even-positioned bits of a 32-bit integer into a 16-bit value."""
    x &= 0x55555555
    x = (x | (x >> 1)) & 0x33333333
    x = (x | (x >> 2)) & 0x0F0F0F0F
    x = (x | (x >> 4)) & 0x00FF00FF
    x = (x | (x >> 8)) & 0x0000FFFF
    return x


def map(x: int, y: int) -> float:
    """Map a 2D coordinate pair to a unique value in [0, 1]."""
    if not (0 <= x <= 0xFFFF) or not (0 <= y <= 0xFFFF):
        raise ValueError("Input coordinates must be in the range [0, 65535].")

    morton_x = _interleave_bits_16(x)
    morton_y = _interleave_bits_16(y) << 1
    morton_code = morton_x | morton_y
    return morton_code / 0xFFFFFFFF


def reverse_map(n: float) -> tuple[int, int]:
    """Decode a value in [0, 1] back into a 2D coordinate pair (x, y)."""
    if not (0.0 <= n <= 1.0):
        raise ValueError("Input value must be in the range [0.0, 1.0].")

    morton_code = int(round(n * 0xFFFFFFFF))
    x = _compact_bits_32(morton_code)
    y = _compact_bits_32(morton_code >> 1)
    return x, y


if __name__ == "__main__":
    example_coords = [
        (0, 0),
        (65535, 65535),
        (65535, 0),
        (0, 65535),
        (12345, 54321),
    ]

    for x, y in example_coords:
        encoded = map(x, y)
        decoded = reverse_map(encoded)
        print(f"map({x}, {y}) = {encoded}")
        print(f"reverse_map({encoded}) = {decoded}")
        assert decoded == (x, y)
        assert map(*decoded) == encoded
        print("round-trip OK\n")

    edge_values = [0.0, 1.0, map(100, 200)]
    for value in edge_values:
        decoded = reverse_map(value)
        encoded = map(*decoded)
        print(f"reverse_map({value}) = {decoded}")
        print(f"map{decoded} = {encoded}\n")
