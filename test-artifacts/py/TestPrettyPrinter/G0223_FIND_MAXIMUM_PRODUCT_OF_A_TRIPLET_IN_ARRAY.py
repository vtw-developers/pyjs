import sys
def f_gold(arr, n):
    if n < 3:
        return -1
    max_product = -(sys.maxsize - 1)
    for i in range(0, n - 2):
        for j in range(i + 1, n - 1):
            for k in range(j + 1, n):
                max_product = max(max_product, arr[i] * arr[j] * arr[k])
    return max_product