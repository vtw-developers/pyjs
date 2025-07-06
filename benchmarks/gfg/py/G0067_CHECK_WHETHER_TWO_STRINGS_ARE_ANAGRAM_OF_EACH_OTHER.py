def test():
  "--- test function ---"
  param =[(['LISTEN'],['SILENT'],),(['TRIANGLE'],['INTEGRAL'],),(['test'],['ttew'],),(['night'],['thing'],),(['Inch'],['Study'],),(['Dusty'],['1'],),(['GJLMOOSTTXaabceefgllpwz'],['EJRXYajoy'],),(['41658699122772743330'],['9931020'],),(['0000000000000000000000001111111111111111111'],['0000000000000000000001111111111111111111111'],),(['ERioPYDqgTSz bVCW'],['GLajZE'],)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str1, str2):
    n1 = len(str1)
    n2 = len(str2)
    if n1 != n2:
        retval_0 = 0
        return retval_0
    str1 = sorted(str1)
    str2 = sorted(str2)
    for i in range(0, n1):
        if str1[i] != str2[i]:
            retval_1 = 0
            return retval_1
    retval_2 = 1
    return retval_2
"-----------------"
test()
