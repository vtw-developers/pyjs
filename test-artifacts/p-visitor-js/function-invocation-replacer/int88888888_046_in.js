function f_gold(x, y) {
    if (y === 0) {
        return 1;
    } else if (y % 2 === 0) {
        const retval_1 = f_gold(x, Math.floor(y / 2)) * f_gold(x, Math.floor(y / 2));
        return retval_1;
    } else {
        const retval_2 = x * f_gold(x, Math.floor(y / 2)) * f_gold(x, Math.floor(y / 2));
        return retval_2;
    }
}