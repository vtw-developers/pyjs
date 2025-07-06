def f_gold(arr, n):
    if n < 1:
        return False
    Min = min(arr)
    Max = max(arr)
    if Max - Min + 1 == n:
        visited = [False for i in range(n)]
        for i in range(n):
            if visited[arr[i] - Min] != False:
                return False
            visited[arr[i] - Min] = True
        return True
    return False