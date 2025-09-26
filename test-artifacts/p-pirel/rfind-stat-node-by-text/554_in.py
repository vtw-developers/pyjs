def f_gold(arr, n):
    hash_0 = dict()
    maximum = 0
    for i in arr:
        if i < 0:
            if abs(i) not in hash_0.keys():
                hash_0[abs(i)] = -1
            else:
                hash_0[abs(i)] -= 1
        else:
            pass