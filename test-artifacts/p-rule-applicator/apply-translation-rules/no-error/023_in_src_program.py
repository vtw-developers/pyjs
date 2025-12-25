def test():
  "--- test function ---"
  param =[(37, 93,),(58, 13,),(89, 27,),(75, 14,),(59, 47,),(84, 39,),(47, 76,),(37, 75,),(83, 62,),(28, 58,),(0, 1,),(1, 0,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(a, b):
    if a == 0:
        myexactlog(1, 0)
        myexactlog(2, b)
        return b
    if b == 0:
        myexactlog(3, 1)
        myexactlog(4, a)
        return a
    k = 0
    myexactlog(5, k)
    while ((a | b) & 1) == 0:
        myexactlog(6, 0)
        a = a >> 1
        myexactlog(7, a)
        b = b >> 1
        myexactlog(8, b)
        k = k + 1
        myexactlog(9, k)
        break
        break
    myexactlog(10, a & 1)
"-----------------"
test()