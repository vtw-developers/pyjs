function f_gold(X, Y, l, r, k, dp) {
    if (k === 0) {
        return 0;
    }
    if (l < 0 || r < 0) {
        return 1000000000;
    }
    if (dp[l][r][k] !== -1) {
        const retval_1 = dp[l][r][k];
        return retval_1;
    }
    const cost = (X.charCodeAt(l) - 'a'.charCodeAt(0)) ^ (Y.charCodeAt(r) - 'a'.charCodeAt(0));
    dp[l][r][k] = Math.min(cost + false, false, false);
    const retval_2 = dp[l][r][k];
    return retval_2;
}