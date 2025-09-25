function f_gold(n) {
  if (n === 0 || n === 9) {
    return true;
  }
  if (n < 9) {
    return false;
  }
  return f_gold((n >> 3) - (n & 7));
}