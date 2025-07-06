def f_gold(keypad, n):
    if not keypad or n <= 0:
        return 0
    if n == 1:
        return 10
    odd = [0] * 10
    even = [0] * 10
    i = 0
    j = 0
    useOdd = 0
    totalCount = 0
    for i in range(10):
        odd[i] = 1
    for j in range(2, n + 1):
        useOdd = 1 - useOdd
        if useOdd == 1:
            even[0] = odd[0] + odd[8]
            even[1] = odd[1] + odd[2] + odd[4]
            even[2] = odd[2] + odd[1] + odd[3] + odd[5]
            even[3] = odd[3] + odd[2] + odd[6]
            even[4] = odd[4] + odd[1] + odd[5] + odd[7]
            even[5] = odd[5] + odd[2] + odd[4] + odd[8] + odd[6]
            even[6] = odd[6] + odd[3] + odd[5] + odd[9]
            even[7] = odd[7] + odd[4] + odd[8]
            even[8] = odd[8] + odd[0] + odd[5] + odd[7] + odd[9]
            even[9] = odd[9] + odd[6] + odd[8]
        else:
            odd[0] = even[0] + even[8]
            odd[1] = even[1] + even[2] + even[4]
            odd[2] = even[2] + even[1] + even[3] + even[5]
            odd[3] = even[3] + even[2] + even[6]
            odd[4] = even[4] + even[1] + even[5] + even[7]
            odd[5] = even[5] + even[2] + even[4] + even[8] + even[6]
            odd[6] = even[6] + even[3] + even[5] + even[9]
            odd[7] = even[7] + even[4] + even[8]
            odd[8] = even[8] + even[0] + even[5] + even[7] + even[9]
            odd[9] = even[9] + even[6] + even[8]
    totalCount = 0
    if useOdd == 1:
        for i in range(10):
            totalCount += even[i]
    else:
        for i in range(10):
            totalCount += odd[i]
    return totalCount