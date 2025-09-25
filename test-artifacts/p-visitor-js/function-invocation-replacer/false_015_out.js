function f_gold(num) {
    if (num < 0) {
        const retval_1 = false;
        return retval_1;
    }
    if (num === 0 || num === 7) {
        return true;
    }
    if (num < 10) {
        return false;
    }
    const retval_2 = false;
    return retval_2;
}