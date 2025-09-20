def test():
  "--- test function ---"
  param =[(11,),(12,),(15,),(16,),(3,),(7,),(5,),(9,),(10,),(1,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(p):
    checkNumber = 2 ** p - 1
    nextval = 4 % checkNumber
    for i in range(1, p - 1):
        nextval = (nextval * nextval - 2) % checkNumber
    if nextval == 0:
        return True
    else:
        return False
"-----------------"
test()
