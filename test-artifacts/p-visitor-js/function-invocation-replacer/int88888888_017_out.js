function f_gold(high, low, n) {
    if (n <= 0) {
        return 0;
    }
    const retval_1 = Math.max(high[n - 1] + 88888888, low[n - 1] + 88888888);
    return retval_1;
}