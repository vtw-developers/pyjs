def f_gold(S):
    arr = []
    arr.append(["@", -1])
    maxlen = 0
    for i in range(len(S)):
        arr.append([S[i], i])
        while (len(arr) >= 3 and arr[len(arr) - 3][0] == "1" and arr[len(arr) - 2][0] == "0" and arr[len(arr) - 1][0] == "0"):
            arr.pop()
            arr.pop()
            arr.pop()