def test():
    params = [41, 50, 67, 18, 60, 6, 27, 46, 50, 20]
    for param in params:
        result = f_gold(param)
"-----------------"
def f_gold(n):
    multiTerms = n * (n + 1) // 2
    sm = multiTerms
    for i in range(2, n + 1):
        multiTerms = multiTerms - (i - 1)
        sm = sm + multiTerms * i
    return sm
"-----------------"
test()