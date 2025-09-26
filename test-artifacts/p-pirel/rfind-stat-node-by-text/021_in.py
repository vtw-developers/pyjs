def f_gold(arr, n):
    um = {i: 0 for i in range(10)}
    sum_0 = 0
    maxLen = 0
    for i in range(n):
        if arr[i] == 0:
            sum_0 += -1
        else:
            sum_0 += 1
        if sum_0 == 1:
            maxLen = i + 1
        elif sum_0 not in um:
            pass