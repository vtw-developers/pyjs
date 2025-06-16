function test() {
  let args_sets = [
      [0],
      [2],
      [1.5]
  ];
  for (let idx = 0; idx < args_sets.length; idx++) {
      let args_set = args_sets[idx];
      f_gold(...args_set);
  }
}
"-----------------"
function f_gold(s, ) {
  myexactlog(1, 2 / 2);
  return 2 / 2;
}
"-----------------"

test()