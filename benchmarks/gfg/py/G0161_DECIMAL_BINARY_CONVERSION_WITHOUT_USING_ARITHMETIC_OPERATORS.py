def test():
  "--- test function ---"
  param =[(35,),(17,),(8,),(99,),(57,),(39,),(99,),(14,),(22,),(7,),(0,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    if n == 0:
        return "0"
    bin_0 = ""
    while n > 0:
        if n & 1 == 0:
            bin_0 = "0" + bin_0
        else:
            bin_0 = "1" + bin_0
        n = n >> 1
    return bin_0
"-----------------"
test()
