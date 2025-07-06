def f_gold(arr, N, k):
    MS = [0 for i in range(N)]
    MS[N - 1] = arr[N - 1]
    for i in range(N - 2, -1, -1):
        if i + k + 1 >= N:
            MS[i] = max(arr[i], MS[i + 1])
        else:
            MS[i] = max(arr[i] + MS[i + k + 1], MS[i + 1])
    return MS[0]