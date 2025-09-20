def test():
  "--- test function ---"
  param =[
     (95, 8, 9, 9,),
     (16, 2, 5, 4,),
     (55, 5, 4, 4,),
     (75, 3, 7, 3,),
     (90, 1, 5, 3,),
     (58, 6, 2, 1,),
     (69, 6, 1, 9,),
     (5, 1, 5, 3,),
     (36, 3, 9, 4,),
     (62, 6, 6, 9,)
  ]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(x, p1, p2, n):
    set1 = (x >> p1) & ((1 << n) - 1)
    set2 = (x >> p2) & ((1 << n) - 1)
    xor = set1 ^ set2
    xor = (xor << p1) | (xor << p2)
    result = x ^ xor
    return result
"-----------------"
test()
