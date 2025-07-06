def test():
  "--- test function ---"
  param =[('pR',),('9518',),('1',),('nNMCIXUCpRMmvO',),('3170487',),('0100101010',),('Z rONcUqWb',),('00419297',),('00',),('r',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    res = ord(str_0[0]) - 48
    for i in range(1, len(str_0)):
        if str_0[i] == "0" or str_0[i] == "1" or res < 2:
            res += ord(str_0[i]) - 48
        else:
            res *= ord(str_0[i]) - 48
    return res
"-----------------"
test()
