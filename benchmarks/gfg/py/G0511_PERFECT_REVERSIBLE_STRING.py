def test():
  "--- test function ---"
  param =[('ab',),('303',),('11110000',),('aba',),('404',),('10101',),('abab',),('6366',),('001',),('',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    i = 0
    j = len(str_0) - 1
    while i < j:
        if str_0[i] != str_0[j]:
            retval_0 = False
            return retval_0
        i += 1
        j -= 1
    retval_1 = True
    return retval_1
"-----------------"
test()
