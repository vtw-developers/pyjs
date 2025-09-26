def f_gold(arr, n, m):
    if n > m:
        return True
    DP = [False for i in range(m)]
    for i in range(n):
        if DP[0]:
            return True
        temp = [False for i in range(m)]
        for j in range(m):
            if DP[j] == True:
                if DP[(j + arr[i]) % m] == False:
                    temp[(j + arr[i]) % m] = True
        for j in range(m):
            if temp[j]:
                DP[j] = True