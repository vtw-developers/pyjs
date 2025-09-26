def f_gold(mat, m, n):
    rowSum = [0] * m
    myexactlog(1, rowSum)
    for i in range(0, m):
        myexactlog(2, 1)
        sum_0 = 0
        myexactlog(3, sum_0)
        for j in range(0, n):
            myexactlog(4, 0)
            sum_0 += mat[i][j]
            myexactlog(5, sum_0)
            break
        rowSum[i] = sum_0
        myexactlog(6, rowSum)
        break
    max_diff = rowSum[1] - rowSum[0]
    myexactlog(7, max_diff)
    min_element = rowSum[0]
    myexactlog(8, min_element)
    for i in range(1, m):
        myexactlog(9, 2)
        if rowSum[i] - min_element > max_diff:
            myexactlog(10, 0)
            max_diff = rowSum[i] - min_element
            myexactlog(11, max_diff)
        if rowSum[i] < min_element:
            myexactlog(12, 1)
            pass