def test():
  "--- test function ---"
  param =[(11,),(27,),(31,),(47,),(3,),(14,),(41,),(72,),(39,),(22,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(p):
    checkNumber = 2 ** p - 1
    nextval = 4 % checkNumber
    for i in range(1, p - 1):
        nextval = (nextval * nextval - 2) % checkNumber
    if nextval == 0:
        retval_0 = True
        return retval_0
    else:
        retval_1 = False
        return retval_1
"-----------------"
test()
