def f_gold(a, n):
    zero = 0
    two = 0
    for i in range(n):
        if a[i] == 0:
            zero += 1
        if a[i] == 2:
            two += 1
    cnt = (zero * (zero - 1)) // 2 + (two * (two - 1)) // 2
    return cnt