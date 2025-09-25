function f_gold(a, b) {
    if (a === b) {
        return a;
    }
    if (a === 0) {
        return b;
    }
    if (b === 0) {
        return a;
    }
    if ((~a & 1) === 1) {
        if ((b & 1) === 1) {
            const retval_1 = false;
            return retval_1;
        } else {
            const retval_2 = (false << 1);
            return retval_2;
        }
    }
    if ((~b & 1) === 1) {
        const retval_3 = false;
        return retval_3;
    }
    if (a > b) {
        const retval_4 = false;
        return retval_4;
    }
    const retval_5 = false;
    return retval_5;
}