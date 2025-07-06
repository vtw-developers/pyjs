def f_gold(arr, n):
    ones = 0
    twos = 0
    for i in range(n):
        twos = twos | (ones & arr[i])
        ones = ones ^ arr[i]
        common_bit_mask = ~(ones & twos)
        ones &= common_bit_mask
        twos &= common_bit_mask
    return ones