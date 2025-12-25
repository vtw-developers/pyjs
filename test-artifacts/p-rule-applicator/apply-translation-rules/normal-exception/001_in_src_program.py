def test():
  "--- test function ---"
  param = [('', 0, -1), ('x', 0, 0), ('1101010101111110', 0, 15)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0, l, h):
    if l > h:
        myexactlog(1, 0)
        retval_1 = sys.maxsize
        myexactlog(2, retval_1)
        myexactlog(3, retval_1)
        return retval_1
    myexactlog(4, l == h)
"-----------------"
test()