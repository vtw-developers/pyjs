def f_gold(arr, n):
    ans = 0
    for i in range(0, n):
        for j in range(i + 1, n):
            if arr[i] == arr[j]:
                ans += 1
    return ans