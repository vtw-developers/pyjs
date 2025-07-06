def f_gold(str_):
    n = len(str_)
    arr = [0] * n
    concat = str_ + str_
    for i in range(n):
        arr[i] = concat[i:n + i]
    arr.sort()
    return arr[0]