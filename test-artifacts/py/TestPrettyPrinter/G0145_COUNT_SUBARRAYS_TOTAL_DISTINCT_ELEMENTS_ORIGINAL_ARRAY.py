def f_gold(arr, n):
    vis = dict()
    for i in range(n):
        vis[arr[i]] = 1
    k = len(vis)
    vid = dict()
    ans = 0
    right = 0
    window = 0
    for left in range(n):
        while right < n and window < k:
            if arr[right] in vid.keys():
                vid[arr[right]] += 1
            else:
                vid[arr[right]] = 1
            if vid[arr[right]] == 1:
                window += 1
            right += 1
        if window == k:
            ans += n - right + 1
        vid[arr[left]] -= 1
        if vid[arr[left]] == 0:
            window -= 1
    return ans