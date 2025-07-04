def f_gold(n):
    bell = [[0 for i in range(n + 1)] for j in range(n + 1)]
    myexactlog(bell)
    bell[0][0] = 1
    myexactlog(bell[0][0])