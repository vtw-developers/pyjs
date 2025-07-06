def test():
  "--- test function ---"
  param =[(6,),(35,),(87,),(91,),(63,),(11,),(66,),(17,),(92,),(81,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    prime = [0] * (n + 1)
    sum_0 = 0
    max_0 = int(n / 2)
    for p in range(2, max_0 + 1):
        if prime[p] == 0:
            for i in range(p * 2, n + 1, p):
                prime[i] = p
    for p in range(2, n + 1):
        if prime[p]:
            sum_0 += prime[p]
        else:
            sum_0 += p
    return sum_0
"-----------------"
test()
