def test():
    params = [20, 68, 52, 61, 3, 88, 41, 78, 94, 18]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(x):
    return -(~x)
"-----------------"
test()