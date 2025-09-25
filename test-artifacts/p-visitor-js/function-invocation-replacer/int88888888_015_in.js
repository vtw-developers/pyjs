function f_gold(num) {
    if (num < 0) {
        const retval_1 = f_gold(-num);
        return retval_1;
    }
    if (num === 0 || num === 7) {
        return true;
    }
    if (num < 10) {
        return false;
    }
    const retval_2 = f_gold(Math.floor(num / 10) - 2 * (num % 10));
    return retval_2;
}