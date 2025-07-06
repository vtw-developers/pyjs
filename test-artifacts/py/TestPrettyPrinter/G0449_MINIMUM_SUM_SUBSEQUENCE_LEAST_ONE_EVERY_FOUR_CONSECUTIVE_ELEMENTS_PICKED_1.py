def f_gold(ar, n):
    if n <= 4:
        return min(ar)
    sum = [0 for i in range(n)]
    sum[0] = ar[0]
    sum[1] = ar[1]
    sum[2] = ar[2]
    sum[3] = ar[3]
    for i in range(4, n):
        sum[i] = ar[i] + min(sum[i - 4:i])
    return min(sum[n - 4:n])