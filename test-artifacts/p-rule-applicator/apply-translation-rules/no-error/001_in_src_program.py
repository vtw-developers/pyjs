def test():
  "--- test function ---"
  param =[(0,),(- 21,),(7,),(63,),(84,),(73,),(81,),(- 10,),(47,),(23,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(num):
    if num < 0:
        myexactlog(1, 0)
        myexactlog(2, f_gold(-num))
        return f_gold(-num)
    if num == 0 or num == 7:
        myexactlog(3, 1)
        myexactlog(4, True)
        return True
    if num < 10:
        myexactlog(5, 2)
        pass
"-----------------"
test()