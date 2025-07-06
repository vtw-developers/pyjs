def test():
  "--- test function ---"
  param =[(50,),(92,),(49,),(94,),(7,),(30,),(88,),(98,),(94,),(23,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    sum_0 = 0
    while n > 0:
        sum_0 += int(n % 10)
        n = int(n / 10)
    return sum_0
"-----------------"
test()
