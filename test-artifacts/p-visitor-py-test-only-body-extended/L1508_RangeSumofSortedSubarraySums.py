arr = []
for i in range(n):
    s = 0
    for j in range(i, n):
        s += nums[j]
        arr.append(s)
arr.sort()
MOD = 10 ** 9 + 7
return sum(arr[left - 1:right]) % MOD