def test():
  "--- test function ---"
  param =[(94,),(94,),(79,),(39,),(16,),(90,),(64,),(76,),(83,),(47,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    odd_count = 0
    even_count = 0
    if n < 0:
        n = -n
    if n == 0:
        retval_0 = 1
        return retval_0
    if n == 1:
        retval_1 = 0
        return retval_1
    while n:
        if n & 1:
            odd_count += 1
        if n & 2:
            even_count += 1
        n = n >> 2
    retval_2 = f_gold(abs(odd_count - even_count))
    return retval_2
"-----------------"
test()
