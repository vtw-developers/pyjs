def test():
  "--- test function ---"
  param =[
     (11, 2, 1),
     (41, 3, 3),
     (5, 4, 3),
     (1, 2, 4),
     (24, 1, 5),
     (5, 2, 3),
     (6, 5, 8),
     (7, 1, 3),
     (7, 3, 10),
     (6, 3, 1),
     (-1, 1, 1)
  ]
  for i, parameters_set in enumerate(param):
    idx = i
    result = f_gold(* parameters_set)
"-----------------"
def f_gold(a, b, k):
    p = a ** b
    count = 0
    while p > 0 and count < k:
        rem = p % 10
        count = count + 1
        if count == k:
            return rem
        p = p / 10
"-----------------"
test()
