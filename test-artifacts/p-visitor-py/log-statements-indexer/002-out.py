def test():
    f_gold()
"-----------------"
def f_gold():
    myexactlog(1, 3, 2, 1)
    print(4, 3, 2)
    myexactlog(2, a, b, c)
    print()
    myexactlog(3, 'a', 'b', 'c')
    print(4, 3, 2)
    myexactlog(4, a=1, b=2)
    print(4, 3, 2)
    myexactlog(5)
"-----------------"
test()