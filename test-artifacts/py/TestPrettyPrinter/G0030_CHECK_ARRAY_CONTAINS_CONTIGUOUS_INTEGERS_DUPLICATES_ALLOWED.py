def f_gold(arr, n):
    max1 = max(arr)
    min1 = min(arr)
    m = max1 - min1 + 1
    if m > n:
        return False
    visited = [0] * m
    for i in range(0, n):
        visited[arr[i] - min1] = True
    for i in range(0, m):
        if visited[i] == False:
            return False
    return True