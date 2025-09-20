def test():
  "--- test function ---"
  param = [([2, 5, 7, 12, 13, 13, 15, 18, 20, 21, 22, 26, 27, 41, 41, 50, 53, 57], 18, 35), ([8, 16, 62, -24, 14, -4], 6, 11), ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 16, 2), ([50, 20, 79, 42, 85, 24, 20, 76, 36, 88, 40, 5, 24, 85], 14, 27), ([-96, -94, -72, -58, -48, -36, -28, -26], 8, 18), ([1, 0, 1], 3, 8), ([2, 7, 8, 15, 18, 23, 24, 25, 27, 35, 40], 11, 32), ([46], 1, 3), ([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 10, 34), ([39, 21, 38, 6, 38, 44], 6, 11)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(arr, n, m):
    if n > m:
        return True
    DP = [False for i in range(m)]
    for i in range(n):
        if DP[0]:
            return True
        temp = [False for i in range(m)]
        for j in range(m):
            if DP[j] == True:
                if DP[(j + arr[i]) % m] == False:
                    temp[(j + arr[i]) % m] = True
        for j in range(m):
            if temp[j]:
                DP[j] = True
        DP[arr[i] % m] = True
    retval_1 = DP[0]
    return retval_1
"-----------------"
test()
