function f_gold(n) {
  if (n === 0 || n === 1) {
    return 1;
  }
  const retval_1 = n * f_gold(n - 2);
  return retval_1;
}