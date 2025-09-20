def test():
  "--- test function ---"
  param =[(6,),(4,),(5,),(2,),(14,),(8,),(1,),(7,),(11,),(12,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(s):
    maxvalue = 0
    i = 1
    for i in range(s - 1):
        j = 1
        for j in range(s):
            k = s - i - j
            maxvalue = max(maxvalue, i * j * k)
    return maxvalue
"-----------------"
test()
