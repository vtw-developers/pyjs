def test():
  "--- test function ---"
  param =[('ba',),('aabb',),('abab',),('aaabb',),('aabbb',),('abaabbaa',),('abaababb',),('bbaa',),('11001000',),('ZWXv te',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    n = len(str_0)
    for i in range(n):
        if str_0[i] != "a":
            break
    if i * 2 != n:
        retval_0 = False
        return retval_0
    for j in range(i, n):
        if str_0[j] != "b":
            retval_1 = False
            return retval_1
    retval_2 = True
    return retval_2
"-----------------"
test()
