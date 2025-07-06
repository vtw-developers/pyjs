def test():
  "--- test function ---"
  param =[(1,),(4,),(64,),(- 64,),(128,),(1024,),(45,),(33,),(66,),(74,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    count = 0
    if n and (not (n & (n - 1))):
        while n > 1:
            n >>= 1
            count += 1
        if count % 2 == 0:
            retval_0 = True
            return retval_0
        else:
            retval_1 = False
            return retval_1
"-----------------"
test()
