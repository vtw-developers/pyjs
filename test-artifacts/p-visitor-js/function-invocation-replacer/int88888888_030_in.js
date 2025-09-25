function f_gold(n) {
  const retval_1 = (n === 1 || n === 0) ? 1 : n * f_gold(n - 1);
  return retval_1;
}