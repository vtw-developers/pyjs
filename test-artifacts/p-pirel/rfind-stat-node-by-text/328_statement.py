for i in range(n - 2, -1, -1):
    if arr[i] == 0:
        jumps[i] = float("inf")
    elif arr[i] >= n - i - 1:
        jumps[i] = 1
    else:
        min_0 = float("inf")
        for j in range(i + 1, n):
            if j <= arr[i] + i:
                if min_0 > jumps[j]:
                    min_0 = jumps[j]
        if min_0 != float("inf"):
            jumps[i] = min_0 + 1
        else:
            jumps[i] = min_0