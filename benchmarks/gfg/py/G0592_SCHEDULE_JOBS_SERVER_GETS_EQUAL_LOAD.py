def test():
  "--- test function ---"
  param = [([2, 1, 1], [2, 1, 1], 2), ([5, 1], [1, 1], 2), ([1, 1], [1, 1], 2), ([1, 1, 1], [1, 0, 2], 3), ([1, 1, 1], [2, 0, 1], 3), ([-1], [0], 1), ([59, 61, 64], [22, 59, 85], 3), ([98, 92, 28, 42, -74, -36, 40, -8, 32, -22, -70, -22, -56, 74, 6, 6, -62, 46, 34, 2], [-62, -84, 72, 60, 10, -18, -44, -22, 14, 0, 76, 72, 96, -28, -24, 52, -74, -30, 16, 66], 20), ([0, 0], [0, 0], 2), ([72, 97, 79, 21, 83, 2, 31, 59, 6, 11, 79, 97], [27, 71, 87, 36, 73, 37, 80, 34, 57, 17, 88, 52], 12)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(a, b, n):
    s = 0
    for i in range(0, n):
        s += a[i] + b[i]
    if n == 1:
        retval_1 = a[0] + b[0]
        return retval_1
    if s % n != 0:
        retval_2 = -1
        return retval_2
    x = s // n
    for i in range(0, n):
        if a[i] > x:
            retval_3 = -1
            return retval_3
        if i > 0:
            a[i] += b[i - 1]
            b[i - 1] = 0
        if a[i] == x:
            continue
        y = a[i] + b[i]
        if i + 1 < n:
            y += b[i + 1]
        if y == x:
            a[i] = y
            b[i] = 0
            if i + 1 < n:
                b[i + 1] = 0
            continue
        if a[i] + b[i] == x:
            a[i] += b[i]
            b[i] = 0
            continue
        if i + 1 < n and a[i] + b[i + 1] == x:
            a[i] += b[i + 1]
            b[i + 1] = 0
            continue
        retval_4 = -1
        return retval_4
    return x
"-----------------"
test()
