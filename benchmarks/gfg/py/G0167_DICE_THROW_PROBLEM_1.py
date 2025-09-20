def test():
  "--- test function ---"
  param = [
     (5, 5, 3,),
     (5, 4, 4,),
     (3, 8, 9,),
     (5, 3, 3,),
     (9, 9, 4,),
     (7, 5, 4,),
     (3, 4, 8,),
     (9, 2, 5,),
     (9, 9, 9,),
     (9, 2, 2,)
  ]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(f, d, s):
    mem = [[0 for i in range(s + 1)] for j in range(d + 1)]
    mem[0][0] = 1
    for i in range(1, d + 1):
        for j in range(1, s + 1):
            mem[i][j] = mem[i][j - 1] + mem[i - 1][j - 1]
            if j - f - 1 >= 0:
                mem[i][j] -= mem[i - 1][j - f - 1]
    retval_1 = mem[d][s]
    return retval_1
"-----------------"
test()
