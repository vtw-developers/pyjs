def f_gold(arr, dep, n):
    arr.sort()
    dep.sort()
    plat_needed = 1
    result = 1
    i = 1
    j = 0
    while i < n and j < n:
        if arr[i] < dep[j]:
            plat_needed += 1
            i += 1
            if plat_needed > result:
                result = plat_needed
        else:
            plat_needed -= 1
            j += 1
    return result