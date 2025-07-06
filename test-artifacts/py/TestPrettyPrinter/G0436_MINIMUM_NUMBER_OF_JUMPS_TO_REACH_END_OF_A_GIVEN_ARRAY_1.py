def f_gold(arr, n):
    jumps = [0 for i in range(n)]
    if (n == 0) or (arr[0] == 0):
        return float("inf")
    jumps[0] = 0
    for i in range(1, n):
        jumps[i] = float("inf")
        for j in range(i):
            if (i <= j + arr[j]) and (jumps[j] != float("inf")):
                jumps[i] = min(jumps[i], jumps[j] + 1)
                break
    return jumps[n - 1]