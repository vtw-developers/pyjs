function f_gold(arr, i, n) {
  if (i > Math.floor((n - 2) / 2)) {
    return true;
  }
  if (
    arr[i] >= arr[2 * i + 1] &&
    arr[i] >= arr[2 * i + 2] &&
    f_gold(arr, 2 * i + 1, n) &&
    f_gold(arr, 2 * i + 2, n)
  ) {
    return true;
  }
  return false;
}