def test():
  "--- test function ---"
  param =[(67,),(77,),(35,),(79,),(45,),(22,),(68,),(17,),(5,),(85,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(num):
    if num // 10 == 0:
        retval_0 = True
        return retval_0
    while num != 0:
        if num // 10 == 0:
            retval_1 = True
            return retval_1
        digit1 = num % 10
        digit2 = (num // 10) % 10
        if abs(digit2 - digit1) > 1:
            retval_2 = False
            return retval_2
        num = num // 10
    retval_3 = True
    return retval_3
"-----------------"
test()
