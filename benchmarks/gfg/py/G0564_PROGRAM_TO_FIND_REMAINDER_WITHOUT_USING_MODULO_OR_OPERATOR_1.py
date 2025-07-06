def test():
  "--- test function ---"
  param =[(34, 55,),(63, 22,),(15, 26,),(56, 58,),(63, 94,),(28, 45,),(54, 97,),(2, 58,),(94, 91,),(82, 40,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(num, divisor):
    if divisor == 0:
        retval_0 = False
        return retval_0
    if divisor < 0:
        divisor = -divisor
    if num < 0:
        num = -num
    i = 1
    product = 0
    while product <= num:
        product = divisor * i
        i += 1
    retval_1 = num - (product - divisor)
    return retval_1
"-----------------"
test()
