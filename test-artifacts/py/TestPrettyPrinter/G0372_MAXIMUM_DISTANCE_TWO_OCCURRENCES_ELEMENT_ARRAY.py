def f_gold(arr, n):
    mp = {}
    maxDict = 0
    for i in range(n):
        if arr[i] not in mp.keys():
            mp[arr[i]] = i
        else:
            maxDict = max(maxDict, i - mp[arr[i]])
    return maxDict