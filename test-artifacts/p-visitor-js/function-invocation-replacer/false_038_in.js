function f_gold(arr, low, high, key) {
    if (high < low) {
        return -1;
    }
    const mid = (low + high) / 2;
    if (key === arr[Math.trunc(mid)]) {
        return mid;
    }
    if (key > arr[Math.trunc(mid)]) {
        return f_gold(arr, (mid + 1), high, key);
    }
    return f_gold(arr, low, (mid - 1), key);
}