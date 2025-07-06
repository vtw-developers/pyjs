def test():
  "--- test function ---"
  param =[('1787075866',),('8',),('1110101110111',),('6673177113',),('7',),('000001',),('dbxMF',),('71733',),('01101101100',),('',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(st):
    l = len(st)
    arr = [0] * l
    for i in range(0, l):
        for j in range(i, l):
            for k in range(j, l):
                if arr[i] % 8 == 0:
                    retval_0 = True
                    return retval_0
                elif (arr[i] * 10 + arr[j]) % 8 == 0 and i != j:
                    retval_1 = True
                    return retval_1
                elif ((arr[i] * 100 + arr[j] * 10 + arr[k]) % 8 == 0 and i != j and j != k and i != k):
                    retval_2 = True
                    return retval_2
    retval_3 = False
    return retval_3
"-----------------"
test()
