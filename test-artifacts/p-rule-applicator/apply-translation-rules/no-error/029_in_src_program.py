def test():
  "--- test function ---"
  param =[(94,),(94,),(79,),(39,),(16,),(90,),(64,),(76,),(83,),(47,),(-1,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(n):
    odd_count = 0
    myexactlog(1, odd_count)
    even_count = 0
    myexactlog(2, even_count)
    if n < 0:
        myexactlog(3, 0)
        n = -n
        myexactlog(4, n)
    if n == 0:
        myexactlog(5, 1)
        myexactlog(6, 1)
        return 1
    if n == 1:
        myexactlog(7, 2)
        myexactlog(8, 0)
        return 0
    while n:
        myexactlog(9, 0)
        if n & 1:
            myexactlog(10, 3)
            odd_count += 1
            myexactlog(11, odd_count)
        if n & 2:
            myexactlog(12, 4)
            even_count += 1
            myexactlog(13, even_count)
        n = n >> 2
        myexactlog(14, n)
    myexactlog(15, f_gold(abs(odd_count - even_count)))
    return f_gold(abs(odd_count - even_count))
"-----------------"
test()