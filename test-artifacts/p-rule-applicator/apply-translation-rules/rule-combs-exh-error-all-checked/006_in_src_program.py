def test():
  "--- test function ---"
  param =[("amazon", "azonam",),("onamaz", "amazon",),("amazon", "azoman",),("ab", "ab",),('737009', '239119',),('000110', '01111',),('l', 'YVo hqvnGxow',),('4420318628', '52856',),('11011111000000', '10',),(' pvFHANc', 'xBIDFbiGb',)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(str1, str2):
    if len(str1) != len(str2):
        myexactlog(1, 0)
        myexactlog(2, False)
        return False
    clock_rot = ""
    myexactlog(3, clock_rot)
    anticlock_rot = ""
    myexactlog(4, anticlock_rot)
    l = len(str2)
    myexactlog(5, l)
    myexactlog(6, anticlock_rot + str2[l - 2:])
"-----------------"
test()