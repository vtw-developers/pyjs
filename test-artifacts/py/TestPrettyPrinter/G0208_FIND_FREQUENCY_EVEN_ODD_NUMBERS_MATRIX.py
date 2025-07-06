def f_gold(ar, m, n):
    even = 0
    odd = 0
    for i in range(m):
        for j in range(n):
            if (ar[i][j] % 2) == 0:
                even += 1
            else:
                odd += 1
    print(" Frequency of odd number =", odd)
    print(" Frequency of even number =", even)