def test():
  "--- test function ---"
  param = [([], 0), ([1, 0], 2), ([1, 1, 1], 3)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(arr, n):
    sum_0 = 0
    maxsize = -1
    for i in range(0, n - 1):
        sum_0 = -1 if (arr[i] == 0) else 1
        for j in range(i + 1, n):
            sum_0 = sum_0 + (-1) if (arr[j] == 0) else sum_0 + 1
            if sum_0 == 0 and maxsize < j - i + 1:
                maxsize = j - i + 1
                startindex = i
    if maxsize == -1:
        print("No such subarray")
    else:
        print(startindex, "to", startindex + maxsize - 1)
    return maxsize
"-----------------"
test()
