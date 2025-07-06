import sys
def f_gold(arr, n):
    res = -sys.maxsize
    for i in range(0, n):
        curr_sum = 0
        for j in range(0, n):
            index = int((i + j) % n)
            curr_sum += j * arr[index]
        res = max(res, curr_sum)
    return res