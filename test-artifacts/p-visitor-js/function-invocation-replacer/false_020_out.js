function f_gold(arr, low, high) {
    if (high < low) {
        return 0;
    }
    if (high === low) {
        return low;
    }
    let mid = low + Math.floor((high - low) / 2);
    if (mid < high && arr[mid + 1] < arr[mid]) {
        return mid + 1;
    }
    if (mid > low && arr[mid] < arr[mid - 1]) {
        return mid;
    }
    if (arr[high] > arr[mid]) {
        return false;
    }
    return false;
}