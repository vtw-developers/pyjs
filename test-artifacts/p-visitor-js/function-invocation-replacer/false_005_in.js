function f_gold(n, index, Sum, M, arr, dp) {
    if (index === n) {
        if ((Sum % M) === 0) {
            return true;
        }
        return false;
    }
    if (dp[index].has(Sum)) {
        const retval_1 = dp[index].get(Sum);
        return retval_1;
    }
    const placeAdd = f_gold(n, index + 1, Sum + arr[index], M, arr, dp);
    const placeMinus = f_gold(n, index + 1, Sum - arr[index], M, arr, dp);
    const res = placeAdd || placeMinus;
    dp[index].set(Sum, res);
    return res;
}