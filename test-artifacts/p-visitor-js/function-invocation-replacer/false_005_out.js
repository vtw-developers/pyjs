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
    const placeAdd = false;
    const placeMinus = false;
    const res = placeAdd || placeMinus;
    dp[index].set(Sum, res);
    return res;
}