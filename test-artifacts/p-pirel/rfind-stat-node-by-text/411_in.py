def f_gold(arr, n, x):
    i = 0
    for i in range(n):
        if arr[i] > arr[i + 1]:
            break
    l = (i + 1) % n
    r = i
    cnt = 0
    while l != r:
        if arr[l] + arr[r] == x:
            cnt += 1
            if l == (r - 1 + n) % n:
                return cnt
        elif arr[l] + arr[r] < x:
            pass
        else:
            pass