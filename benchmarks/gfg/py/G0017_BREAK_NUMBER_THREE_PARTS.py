def test():
  "--- test function ---"
  param =[(10,),(13,),(17,),(3,),(5,),(7,),(11,),(2,),(19,),(23,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    count = 0
    for i in range(0, n + 1):
        for j in range(0, n + 1):
            for k in range(0, n + 1):
                if i + j + k == n:
                    count = count + 1
    return count
"-----------------"
test()
