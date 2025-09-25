function f_gold(str_0, l, h) {
    if (l > h) {
        const retval_1 = Number.MAX_SAFE_INTEGER;
        return retval_1;
    }
    if (l === h) {
        return 0;
    }
    if (l === h - 1) {
        const retval_2 = (str_0[l] === str_0[h]) ? 0 : 1;
        return retval_2;
    }
    if (str_0[l] === str_0[h]) {
        const retval_3 = false;
        return retval_3;
    } else {
        const retval_4 = Math.min(false, false) + 1;
        return retval_4;
    }
}