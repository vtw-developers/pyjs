def f_gold(arr, n):
    mp = dict()
    Sum = 0
    count = 0
    for i in range(n):
        if arr[i] == 0:
            arr[i] = -1
        Sum += arr[i]
        if Sum == 0:
            count += 1
        if Sum in mp.keys():
            count += mp[Sum]
        mp[Sum] = mp.get(Sum, 0) + 1
    return count