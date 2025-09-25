function f_gold(arr, n) {
    if (n <= 1) return;
    false;
    const last = arr[n - 1];
    let j = n - 2;
    while (j >= 0 && arr[j] > last) {
        arr[j + 1] = arr[j];
        j = j - 1;
    }
    arr[j + 1] = last;
}