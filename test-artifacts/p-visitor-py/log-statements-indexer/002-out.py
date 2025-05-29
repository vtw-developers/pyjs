def test():
    f_gold()
"-----------------"
def f_gold():
    myexactlog(1, 3, 2, 1)
    print(2, 4, 3, 2)
    myexactlog(3, a, b, c)
    print(4)
    myexactlog(5, 'a', 'b', 'c')
    print(6, 4, 3, 2)
    myexactlog(7, a=1, b=2)
    print(8, 4, 3, 2)
    myexactlog(9)
"-----------------"
test()