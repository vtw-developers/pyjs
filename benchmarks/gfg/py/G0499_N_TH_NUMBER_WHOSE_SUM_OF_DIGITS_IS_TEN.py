def test():
  "--- test function ---"
  param =[(37,),(13,),(51,),(69,),(76,),(10,),(97,),(40,),(69,),(4,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import itertools
def f_gold(n):
    count = 0
    nat = itertools.count()
    curr = next(nat)
    while count != n:
        sum_0 = 0
        x = curr
        curr = next(nat)
        while x:
            sum_0 = sum_0 + x % 10
            x = x // 10
        if sum_0 == 10:
            count = count + 1
    return curr
"-----------------"
test()
