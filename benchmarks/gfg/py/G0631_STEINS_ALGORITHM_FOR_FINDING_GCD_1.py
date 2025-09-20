def test():
  "--- test function ---"
  param =[(52, 29,),(36, 94,),(12, 6,),(69, 7,),(45, 11,),(7, 51,),(45, 55,),(62, 86,),(96, 63,),(89, 12,),(0, 1,),(1, 0,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(a, b):
    if a == b:
        return a
    if a == 0:
        return b
    if b == 0:
        return a
    if (~a & 1) == 1:
        if (b & 1) == 1:
            retval_1 = f_gold(a >> 1, b)
            return retval_1
        else:
            retval_2 = f_gold(a >> 1, b >> 1) << 1
            return retval_2
    if (~b & 1) == 1:
        retval_3 = f_gold(a, b >> 1)
        return retval_3
    if a > b:
        retval_4 = f_gold((a - b) >> 1, b)
        return retval_4
    retval_5 = f_gold((b - a) >> 1, a)
    return retval_5
"-----------------"
test()
