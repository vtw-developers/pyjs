function f_gold(high, low, n) {
    if (n <= 0) {
        return 0;
    }
    const retval_1 = Math.max(high[n - 1] + false, low[n - 1] + false);
    return retval_1;
}