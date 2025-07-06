def f_gold(arr, n):
    if n <= 0:
        return 0
    incl = arr[0]
    excl = 0
    for i in range(1, n):
        incl_new = arr[i] + min(excl, incl)
        excl_new = incl
        incl = incl_new
        excl = excl_new
    return min(incl, excl)