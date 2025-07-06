def f_gold(mat, n, sum):
    for i in range(n):
        mat[i].sort()
    for i in range(n - 1):
        for j in range(i + 1, n):
            left = 0
            right = n - 1
            while left < n and right >= 0:
                if (mat[i][left] + mat[j][right]) == sum:
                    print("(", mat[i][left], ", ", mat[j][right], "), ", end=" ")
                    left += 1
                    right -= 1
                else:
                    if (mat[i][left] + mat[j][right]) < sum:
                        left += 1
                    else:
                        right -= 1