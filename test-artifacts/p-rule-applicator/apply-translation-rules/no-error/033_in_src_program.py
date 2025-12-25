def test():
  "--- test function ---"
  param = [([2, 1, 1], [2, 1, 1], 2), ([5, 1], [1, 1], 2), ([1, 1], [1, 1], 2), ([1, 1, 1], [1, 0, 2], 3), ([1, 1, 1], [2, 0, 1], 3), ([-1], [0], 1), ([59, 61, 64], [22, 59, 85], 3), ([98, 92, 28, 42, -74, -36, 40, -8, 32, -22, -70, -22, -56, 74, 6, 6, -62, 46, 34, 2], [-62, -84, 72, 60, 10, -18, -44, -22, 14, 0, 76, 72, 96, -28, -24, 52, -74, -30, 16, 66], 20), ([0, 0], [0, 0], 2), ([72, 97, 79, 21, 83, 2, 31, 59, 6, 11, 79, 97], [27, 71, 87, 36, 73, 37, 80, 34, 57, 17, 88, 52], 12)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(a, b, n):
    s = 0
    myexactlog(1, s)
    for i in range(0, n):
        myexactlog(2, 0)
        s += a[i] + b[i]
        myexactlog(3, s)
    if n == 1:
        myexactlog(4, 0)
        retval_1 = a[0] + b[0]
        myexactlog(5, retval_1)
        myexactlog(6, retval_1)
        return retval_1
    if s % n != 0:
        myexactlog(7, 1)
        retval_2 = -1
        myexactlog(8, retval_2)
        myexactlog(9, retval_2)
        return retval_2
    x = s // n
    myexactlog(10, x)
"-----------------"
test()