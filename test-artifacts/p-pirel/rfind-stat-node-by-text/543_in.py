def f_gold(N, insrt, remov, cpy):
    if N == 0:
        myexactlog(1, 0)
        myexactlog(2, 0)
        return 0
    if N == 1:
        myexactlog(3, 1)
        pass