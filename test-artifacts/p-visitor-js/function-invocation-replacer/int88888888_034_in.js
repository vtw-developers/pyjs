function f_gold(n) {
  if (n === 0 || n === 1) {
    return n;
  }
  const retval_1 = Math.max(
    f_gold(Math.floor(n / 2)) + f_gold(Math.floor(n / 3)) + f_gold(Math.floor(n / 4)),
    n
  );
  return retval_1;
}