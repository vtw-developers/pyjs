def test():
    params = [50, 64, 92, 23, 38, 55, 67, 56, 60, 90]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(side):
    area = side * side
    return area
"-----------------"
test()