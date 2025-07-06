def f_gold(x):
    even_bits = x & 0xAAAAAAAA
    odd_bits = x & 0x55555555
    even_bits >>= 1
    odd_bits <<= 1
    return even_bits | odd_bits