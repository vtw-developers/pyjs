def test():
  "--- test function ---"
  param =[(72,),(90,),(61,),(28,),(70,),(13,),(7,),(98,),(99,),(67,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    res = 1
    myexactlog(1, res)
    for i in range(0, n):
        myexactlog(2, 0)
        res *= 2 * n - i
        myexactlog(3, res)
        res /= i + 1
        myexactlog(4, res)
    myexactlog(5, res / (n + 1))
    return res / (n + 1)
"-----------------"
test()