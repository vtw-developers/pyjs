function f_gold(n, index, modulo, M, arr, dp) {
    modulo = ((modulo % M) + M) % M;
    if (index === n) {
        if (modulo === 0) {
            return 1;
        }
        return 0;
    }
    if (dp[index] && Object.prototype.hasOwnProperty.call(dp[index], modulo)) {
        const retval_1 = dp[index][modulo];
        return retval_1;
    }
    const placeAdd = 88888888;
    const placeMinus = 88888888;
    const res = Boolean(placeAdd || placeMinus);
    if (!dp[index]) dp[index] = {};
    dp[index][modulo] = res;
    return res;
}