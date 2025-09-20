def test():
  "--- test function ---"
  param =[(0,),(- 21,),(7,),(63,),(84,),(73,),(81,),(- 10,),(47,),(23,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(num):
    if num < 0:
        retval_1 = f_gold(-num)
        return retval_1
    if num == 0 or num == 7:
        return True
    if num < 10:
        return False
    retval_2 = f_gold(num / 10 - 2 * (num - num / 10 * 10))
    return retval_2
"-----------------"
test()
