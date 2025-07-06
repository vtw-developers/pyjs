def test():
  "--- test function ---"
  param =[(13,),(27,),(1,),(24,),(98,),(94,),(36,),(41,),(74,),(39,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    count = 0
    if n and not (n & (n - 1)):
        return n
    while n != 0:
        n >>= 1
        count += 1
    retval_0 = 1 << count
    return retval_0
"-----------------"
test()
