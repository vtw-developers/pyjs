def f_gold(arr, n):
    fw = [0 for k in range(n)]
    bw = [0 for k in range(n)]
    cur_max, max_so_far = arr[0], arr[0]
    for i in range(n):
        cur_max = max(arr[i], cur_max + arr[i])
        max_so_far = max(max_so_far, cur_max)
        fw[i] = cur_max
    cur_max = max_so_far = bw[n - 1] = arr[n - 1]
    i = n - 2
    while i >= 0:
        cur_max = max(arr[i], cur_max + arr[i])
        max_so_far = max(max_so_far, cur_max)
        bw[i] = cur_max
        i -= 1
    fans = max_so_far
    for i in range(1, n - 1):
        fans = max(fans, fw[i - 1] + bw[i + 1])
    return fans