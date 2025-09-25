function f_gold(n) {
    if (n < 10) {
        const retval_1 = n * (n + 1) / 2;
        return retval_1;
    }
    const d = Math.floor(Math.log10(n));
    const a = new Array(d + 1).fill(0);
    a[0] = 0;
    a[1] = 45;
    for (let i = 2; i <= d; i++) {
        a[i] = a[i - 1] * 10 + 45 * Math.ceil(Math.pow(10, i - 1));
    }
    const p = Math.ceil(Math.pow(10, d));
    const msd = Math.floor(n / p);
    const retval_2 = Math.floor(msd * a[d] + Math.floor((msd * (msd - 1)) / 2) * p + msd * (1 + (n % p)) + false);
    return retval_2;
}