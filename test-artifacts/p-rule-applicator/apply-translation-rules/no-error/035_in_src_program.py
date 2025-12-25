def test():
  "--- test function ---"
  param =[('()',),('))((',),('())',),('(()',),('(()()())',),('))())(()(())',),('))(())((',),('49',),('00001111',),('KDahByG ',),('',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(s):
    myexactlog(1, len(s))
"-----------------"
test()