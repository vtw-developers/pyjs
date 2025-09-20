def test():
  "--- test function ---"
  param =[(93,),(10,),(55,),(94,),(2,),(5,),(37,),(4,),(11,),(46,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    count = 0
    curr = 19
    while True:
        sum_0 = 0
        x = curr
        while x > 0:
            sum_0 = sum_0 + x % 10
            x = int(x / 10)
        if sum_0 == 10:
            count += 1
        if count == n:
            return curr
        curr += 9
    retval_1 = -1
    return retval_1
"-----------------"
test()
