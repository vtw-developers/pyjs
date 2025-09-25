function f_gold(arr, l, r, x) {
    if (r >= l) {
        const mid = l + Math.floor((r - l) / 2);
        if (arr[mid] === x) {
            return mid;
        } else if (arr[mid] > x) {
            return false;
        } else {
            return false;
        }
    } else {
        return -1;
    }
}