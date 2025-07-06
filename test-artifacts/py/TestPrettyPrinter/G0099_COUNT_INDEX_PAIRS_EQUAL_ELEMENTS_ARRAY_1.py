def f_gold(arr, n):
    mp = dict()
    for i in range(n):
        if arr[i] in mp.keys():
            mp[arr[i]] += 1
        else:
            mp[arr[i]] = 1
    ans = 0
    for it in mp:
        count = mp[it]
        ans += (count * (count - 1)) // 2
    return ans