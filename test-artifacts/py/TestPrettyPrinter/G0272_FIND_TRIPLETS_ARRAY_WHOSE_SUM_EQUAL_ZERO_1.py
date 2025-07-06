def f_gold(arr, n):
    found = False
    for i in range(n - 1):
        s = set()
        for j in range(i + 1, n):
            x = -(arr[i] + arr[j])
            if x in s:
                print(x, arr[i], arr[j])
                found = True
            else:
                s.add(arr[j])
    if found == False:
        print("No Triplet Found")