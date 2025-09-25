function f_gold(n) {
  n = BigInt(n);
  let odd_count = 0n;
  let even_count = 0n;
  if (n < 0n) {
    n = -n;
  }
  if (n === 0n) {
    return 1;
  }
  if (n === 1n) {
    return 0;
  }
  while (n) {
    if (n & 1n) {
      odd_count += 1n;
    }
    if (n & 2n) {
      even_count += 1n;
    }
    n = n >> 2n;
  }
  const diff = odd_count >= even_count ? odd_count - even_count : even_count - odd_count;
  return f_gold(diff);
}