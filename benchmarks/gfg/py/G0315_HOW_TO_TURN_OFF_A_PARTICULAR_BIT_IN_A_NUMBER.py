def test():
  "--- test function ---"
  param =[
     (49, 15,),
     (59, 6,),
     (76, 2,),
     (27, 7,),
     (61, 6,),
     (67, 2,),
     (63, 7,),
     (85, 2,),
     (90, 6,),
     (24, 5,),
     (0, 0,)
  ]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n, k):
    if k <= 0:
        return n
    retval_1 = n & ~(1 << (k - 1))
    return retval_1
"-----------------"
test()
