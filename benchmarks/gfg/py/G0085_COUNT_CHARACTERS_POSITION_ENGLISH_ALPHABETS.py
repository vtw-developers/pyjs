def test():
  "--- test function ---"
  param =[('lLkhFeZGcb',),('ABcED',),('geeksforgeeks',),('Alphabetical',),('abababab',),('bcdefgxyz',),('cBzaqx L',),(' bcd',),('11',),('MqqKY',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str_0):
    result = 0
    for i in range(len(str_0)):
        if (i == ord(str_0[i]) - ord("a")) or (i == ord(str_0[i]) - ord("A")):
            result += 1
    return result
"-----------------"
test()
