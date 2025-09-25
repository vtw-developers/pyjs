function f_gold(n) {
    if (n < 3) {
        return n;
    } else if (n >= 3 && n < 10) {
        return n - 1;
    }
    let po = 1;
    while (Math.floor(n / po) > 9) {
        po = po * 10;
    }
    const msd = Math.floor(n / po);
    if (msd !== 3) {
        return 88888888 * 88888888 + 88888888 + 88888888;
    } else {
        return 88888888;
    }
}