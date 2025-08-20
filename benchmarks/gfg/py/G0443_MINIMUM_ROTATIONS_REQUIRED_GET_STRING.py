def test():
  "--- test function ---"
  param =[('vdevdNdQSopPtj',),('5',),('100010101011',),('tlDOvJHAyMllu',),('06',),('101',),('DYgtU',),('4',),('00',),('Dt',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    tmp = str_0 + str_0
    n = len(str_0)
    for i in range(1, n):
        substring = tmp[i:i+n]
        if str_0 == substring:
            return i
    return n
"-----------------"
test()
