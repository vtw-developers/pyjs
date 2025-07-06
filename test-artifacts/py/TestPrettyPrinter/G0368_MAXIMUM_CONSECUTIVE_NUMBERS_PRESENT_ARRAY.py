def f_gold(arr, n):
    S = set()
    for i in range(n):
        S.add(arr[i])
    ans = 0
    for i in range(n):
        if S.__contains__(arr[i]):
            j = arr[i]
            while S.__contains__(j):
                j += 1
            ans = max(ans, j - arr[i])
    return ans