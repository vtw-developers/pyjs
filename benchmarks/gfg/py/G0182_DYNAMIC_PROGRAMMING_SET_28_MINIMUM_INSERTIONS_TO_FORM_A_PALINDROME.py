def test():
  "--- test function ---"
  param = [('', 0, -1), ('x', 0, 0), ('1101010101111110', 0, 15)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import sys
def f_gold(str_0, l, h):
    if l > h:
        retval_1 = sys.maxsize
        return retval_1
    if l == h:
        return 0
    if l == h - 1:
        retval_2 = 0 if (str_0[l] == str_0[h]) else 1
        return retval_2
    if str_0[l] == str_0[h]:
        retval_3 = f_gold(str_0, l + 1, h - 1)
        return retval_3
    else:
        retval_4 = min(f_gold(str_0, l, h - 1), f_gold(str_0, l + 1, h)) + 1
        return retval_4
"-----------------"
test()
