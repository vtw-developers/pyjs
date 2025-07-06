def f_gold(arr, n):
    l = 0
    _sum = 0
    ans = 360
    for i in range(n):
        _sum += arr[i]
        while _sum >= 180:
            ans = min(ans, 2 * abs(180 - _sum))
            _sum -= arr[l]
            l += 1
        ans = min(ans, 2 * abs(180 - _sum))
    return ans