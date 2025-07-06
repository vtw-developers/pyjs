def f_gold(mat, m, n):
    rowSum = [0] * m
    for i in range(0, m):
        sum = 0
        for j in range(0, n):
            sum += mat[i][j]
        rowSum[i] = sum
    max_diff = rowSum[1] - rowSum[0]
    min_element = rowSum[0]
    for i in range(1, m):
        if rowSum[i] - min_element > max_diff:
            max_diff = rowSum[i] - min_element
        if rowSum[i] < min_element:
            min_element = rowSum[i]
    return max_diff