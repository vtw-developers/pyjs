def f_gold(arr, n):
    jumps = [0 for i in range(n)]
    for i in range(n - 2, -1, -1):
        if arr[i] == 0:
            jumps[i] = float("inf")
        elif arr[i] >= n - i - 1:
            pass
        else:
            pass