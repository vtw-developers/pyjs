while (len(arr) >= 3 and arr[len(arr) - 3][0] == "1" and arr[len(arr) - 2][0] == "0" and arr[len(arr) - 1][0] == "0"):
    arr.pop()
    arr.pop()
    arr.pop()