def test():
  "--- test function ---"
  param =[('IVQPwMhUYLDTcO',),('2568689919714',),('0110011',),('CSUPHnJs',),('67978022339633',),('0110011101',),('RgR',),('62249378',),('000110110',),('IRcBQAUdiyKrz',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    n = len(str_0)
    myexactlog(1, n)
    myexactlog(2, range(n))
"-----------------"
test()