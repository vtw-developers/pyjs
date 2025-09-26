def test():
  "--- test function ---"
  param =[(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    a = [0] * n
    b = [0] * n
    a[0] = b[0] = 1
    for i in range(1, n):
        a[i] = a[i - 1] + b[i - 1]
        b[i] = a[i - 1]
    retval_1 = (1 << n) - a[n - 1] - b[n - 1]
    return retval_1
"-----------------"
test()
