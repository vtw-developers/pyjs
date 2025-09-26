def f_gold(arr, n):
    found = False
    arr.sort()
    for i in range(0, n - 1):
        l = i + 1
        r = n - 1
        x = arr[i]
        while l < r:
            if x + arr[l] + arr[r] == 0:
                print(x, arr[l], arr[r])
                l += 1
                r -= 1
                found = True
            elif x + arr[l] + arr[r] < 0:
                pass
            else:
                pass