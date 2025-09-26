def test():
  "--- test function ---"
  param =[(1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    C = [[0 for x in range(n + 1)] for y in range(n + 1)]
    for i in range(0, n + 1):
        for j in range(0, min(i, n + 1)):
            if j == 0 or j == i:
                C[i][j] = 1
            else:
                C[i][j] = C[i - 1][j - 1] + C[i - 1][j]
    sum_0 = 0
    for i in range(0, n + 1):
        if n % 2 == 0:
            sum_0 = sum_0 + C[n][i]
    return sum_0
"-----------------"
test()
