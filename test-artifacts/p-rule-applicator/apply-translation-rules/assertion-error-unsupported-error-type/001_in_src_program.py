def test():
  "--- test function ---"
  param =[(20,),(6,),(39,),(80,),(88,),(7,),(16,),(27,),(83,),(6,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
import math
def f_gold(n):
    res = 1
    myexactlog(1, res)
    while n % 2 == 0:
        myexactlog(2, 0)
        n = n // 2
        myexactlog(3, n)
    for i in range(3, int(math.sqrt(n) + 1)):
        myexactlog(4, 0)
        count = 0
        myexactlog(5, count)
        curr_sum = 1
        myexactlog(6, curr_sum)
        curr_term = 1
        myexactlog(7, curr_term)
        while n % i == 0:
            myexactlog(8, 1)
            count += 1
            myexactlog(9, count)
            n = n // i
            myexactlog(10, n)
            curr_term *= i
            myexactlog(11, curr_term)
            curr_sum += curr_term
            myexactlog(12, curr_sum)
        res *= curr_sum
        myexactlog(13, res)
    if n >= 2:
        myexactlog(14, 0)
        res *= 1 + n
        myexactlog(15, res)
    myexactlog(16, res)
    return res
"-----------------"
test()