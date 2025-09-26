def test():
  "--- test function ---"
  param =[(492.762671782271, 4,),(- 88.1149138859112, 4,),(889.981827152698, 4,),(- 704.090587314416, 4,),(921.145968063258, 4,),(- 473.690018081376, 4,),(321.586891359318, 4,),(- 406.1025383282854, 4,),(786.145296436601, 4,),(- 1.421835366018, -1,)]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(x, y):
    if y == 0:
        return 1
    temp = f_gold(x, int(y / 2))
    if y % 2 == 0:
        retval_1 = temp * temp
        return retval_1
    else:
        if y > 0:
            retval_2 = x * temp * temp
            return retval_2
        else:
            retval_3 = (temp * temp) / x
            return retval_3
"-----------------"
test()
