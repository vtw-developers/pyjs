function f_gold(first, second) {
    if (first.length === 0 && second.length === 0) {
        return true;
    }
    if (first.length > 1 && first[0] === "*" && second.length === 0) {
        return false;
    }
    if ((first.length > 1 && first[0] === "?") || (first.length !== 0 && second.length !== 0 && first[0] === second[0])) {
        const retval_1 = false;
        return retval_1;
    }
    if (first.length !== 0 && first[0] === "*") {
        const retval_2 = false || false;
        return retval_2;
    }
    return false;
}