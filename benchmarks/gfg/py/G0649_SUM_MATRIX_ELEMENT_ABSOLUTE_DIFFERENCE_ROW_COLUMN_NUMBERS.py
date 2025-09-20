def test():
  "--- test function ---"
  param =[(6,),(4,),(7,),(9,),(8,),(5,),(2,),(1,),(3,),(10,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    arr = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            arr[i][j] = abs(i - j)
    sum_0 = 0
    for i in range(n):
        for j in range(n):
            sum_0 += arr[i][j]
    return sum_0
"-----------------"
test()
