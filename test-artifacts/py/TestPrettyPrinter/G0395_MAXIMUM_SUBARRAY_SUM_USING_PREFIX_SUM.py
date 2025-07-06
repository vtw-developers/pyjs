import math
def f_gold(arr, n):
    min_prefix_sum = 0
    res = -math.inf
    prefix_sum = []
    prefix_sum.append(arr[0])
    for i in range(1, n):
        prefix_sum.append(prefix_sum[i - 1] + arr[i])
    for i in range(n):
        res = max(res, prefix_sum[i] - min_prefix_sum)
        min_prefix_sum = min(min_prefix_sum, prefix_sum[i])
    return res