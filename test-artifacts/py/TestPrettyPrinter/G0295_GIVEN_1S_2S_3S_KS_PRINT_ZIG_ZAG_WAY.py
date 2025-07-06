def f_gold(rows, columns, numbers):
    k = 0
    arr = [[0 for i in range(columns)] for j in range(rows)]
    for i in range(rows):
        if i % 2 == 0:
            j = 0
            while j < columns and numbers[k] > 0:
                arr[i][j] = k + 1
                numbers[k] -= 1
                if numbers[k] == 0:
                    k += 1
                j += 1
        else:
            j = columns - 1
            while j >= 0 and numbers[k] > 0:
                arr[i][j] = k + 1
                numbers[k] -= 1
                if numbers[k] == 0:
                    k += 1
                j -= 1
    for i in arr:
        for j in i:
            print(j, end=" ")
        print()