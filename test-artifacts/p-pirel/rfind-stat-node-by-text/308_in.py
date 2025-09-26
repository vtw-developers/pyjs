def f_gold(n, templeHeight):
    sum_0 = 0
    for i in range(n):
        left = 0
        right = 0
        for j in range(i - 1, -1, -1):
            if templeHeight[j] < templeHeight[j + 1]:
                left += 1
            else:
                break
        for j in range(i + 1, n):
            if templeHeight[j] < templeHeight[j - 1]:
                right += 1
            else:
                break
        sum_0 += max(right, left) + 1