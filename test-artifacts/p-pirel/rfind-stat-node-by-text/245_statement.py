while l != r:
    if arr[l] + arr[r] == x:
        cnt += 1
        if l == (r - 1 + n) % n:
            return cnt
        l = (l + 1) % n
        r = (r - 1 + n) % n
    elif arr[l] + arr[r] < x:
        l = (l + 1) % n
    else:
        r = (n + r - 1) % n