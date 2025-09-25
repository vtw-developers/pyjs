function f_gold(no) {
    return no === 0 ? 0 : Math.trunc(((no % 10) + 10) % 10) + f_gold(Math.trunc(no / 10));
}