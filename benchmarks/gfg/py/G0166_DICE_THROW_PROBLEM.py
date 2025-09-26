def test():
  "--- test function ---"
  param =[(4, 4, 4,),(7, 12, 3,),(2, 4, 4,),(9, 9, 8,),(5, 5, 2,),(3, 9, 2,),(4, 2, 6,),(8, 5, 8,),(4, 8, 7,),(6, 8, 1,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(m, n, x):
    table = [[0] * (x + 1) for i in range(n + 1)]
    for j in range(1, min(m + 1, x + 1)):
        table[1][j] = 1
    for i in range(2, n + 1):
        for j in range(1, x + 1):
            for k in range(1, min(m + 1, j)):
                table[i][j] += table[i - 1][j - k]
    retval_1 = table[-1][-1]
    return retval_1
"-----------------"
test()
