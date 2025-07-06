def f_gold(arr, n):
    remainder = 0
    for i in range(0, n):
        remainder = (remainder + arr[i]) % 3
    return remainder == 0