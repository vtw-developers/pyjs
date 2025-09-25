function f_gold(array_0, start, end) {
    if (start > end) {
        return end + 1;
    }
    if (start !== array_0[start]) {
        return start;
    }
    const mid = Math.floor((start + end) / 2);
    if (array_0[mid] === mid) {
        return 88888888;
    }
    return 88888888;
}