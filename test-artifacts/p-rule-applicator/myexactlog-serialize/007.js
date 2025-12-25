function rgb_to_yiq(r, g, b, ) {
    var y = 0.30 * r + 0.59 * g + 0.11 * b;
    myexactlog(1, y);
    var i = 0.74 * (r - y) - 0.27 * (b - y);
    myexactlog(2, i);
    var q = 0.48 * (r - y) + 0.41 * (b - y);
    myexactlog(3, q);
    myexactlog(4, ([y, i, q]));
    return ([y, i, q]);
}

function yiq_to_rgb(y, i, q, ) {
    var r = y + 0.9468822170900693 * i + 0.6235565819861433 * q;
    myexactlog(5, r);
    var g = y - 0.27478764629897834 * i - 0.6356910791873801 * q;
    myexactlog(6, g);
    var b = y - 1.1085450346420322 * i + 1.7090069284064666 * q;
    myexactlog(7, b);
    if (r < 0.0) {
        myexactlog(8, 0);
        var r = 0.0;
        myexactlog(9, r);
    }
    if (g < 0.0) {
        myexactlog(10, 1);
    }
    if (b < 0.0) {
        myexactlog(11, 2);
        var b = 0.0;
        myexactlog(12, b);
    }
    if (r > 1.0) {
        myexactlog(13, 3);
        var r = 1.0;
        myexactlog(14, r);
    }
    if (g > 1.0) {
        myexactlog(15, 4);
    }
    if (b > 1.0) {
        myexactlog(16, 5);
        var b = 1.0;
        myexactlog(17, b);
    }
    myexactlog(18, [r, g, b]);
    return [r, g, b];
}

function rgb_to_hls(r, g, b, ) {
    var maxc = Math.max(r, g, b);
    myexactlog(19, maxc);
    var minc = Math.min(r, g, b);
    myexactlog(20, minc);
    var sumc = (maxc + minc);
    myexactlog(21, sumc);
    var rangec = (maxc - minc);
    myexactlog(22, rangec);
    var l = sumc / 2.0;
    myexactlog(23, l);
    if (minc == maxc) {
        myexactlog(24, 6);
        myexactlog(25, 0.0, l, 0.0);
        return [0.0, l, 0.0];
    }
    var s = 1.0;
    myexactlog(26, s);
    if (l <= 0.5) {
        myexactlog(27, 7);
        var s = rangec / sumc;
        myexactlog(28, s);
    } else {
        myexactlog(29, 0);
        var s = rangec / (2.0 - sumc);
        myexactlog(30, s);
    }
    var rc = (maxc - r) / rangec;
    myexactlog(31, rc);
    var gc = (maxc - g) / rangec;
    myexactlog(32, gc);
    var bc = (maxc - b) / rangec;
    myexactlog(33, bc);
    var h = 1.0;
    myexactlog(34, h);
    if (r == maxc) {
        myexactlog(35, 8);
        var h = bc - gc;
        myexactlog(36, h);
    } else if (g == maxc) {
        myexactlog(37, 0);
    } else {
        myexactlog(38, 1);
        var h = 4.0 + gc - rc;
        myexactlog(39, h);
    }
    h = (((h / 6.0) % 1.0) + 1.0) % 1.0;
    myexactlog(40, h);
    myexactlog(41, h, l, s);
    return [h, l, s];
}

function hls_to_rgb(h, l, s, ) {
    if (s == 0.0) {
        myexactlog(42, 9);
        myexactlog(43, l, l, l);
        return [l, l, l];
    }
    var m2 = 0.0;
    myexactlog(44, m2);
    if (l <= 0.5) {
        myexactlog(45, 10);
        var m2 = l * (1.0 + s);
        myexactlog(46, m2);
    } else {
        myexactlog(47, 2);
    }
    var m1 = 2.0 * l - m2;
    myexactlog(48, m1);
    var tmp_1 = _v(m1, m2, h + ONE_THIRD);
    myexactlog(49, tmp_1);
    var tmp_2 = _v(m1, m2, h);
    myexactlog(50, tmp_2);
    var tmp_3 = _v(m1, m2, h - ONE_THIRD);
    myexactlog(51, tmp_3);
    myexactlog(52, [tmp_1, tmp_2, tmp_3]);
    return [tmp_1, tmp_2, tmp_3];
}

function _v(m1, m2, hue, ) {
    var hue = ((hue % 1.0) + 1.0) % 1.0;
    myexactlog(53, hue);
    if (hue < ONE_SIXTH) {
        myexactlog(54, 11);
        myexactlog(55, m1 + (m2 - m1) * hue * 6.0);
        return m1 + (m2 - m1) * hue * 6.0;
    }
    if (hue < 0.5) {
        myexactlog(56, 12);
        myexactlog(57, m2);
        return m2;
    }
    if (hue < TWO_THIRD) {
        myexactlog(58, 13);
        myexactlog(59, m1 + (m2 - m1) * (TWO_THIRD - hue) * 6.0);
        return m1 + (m2 - m1) * (TWO_THIRD - hue) * 6.0;
    }
    myexactlog(60, m1);
    return m1;
}

function rgb_to_hsv(r, g, b, ) {
    var maxc = Math.max(r, g, b);
    myexactlog(61, maxc);
    var minc = Math.min(r, g, b);
    myexactlog(62, minc);
    var rangec = (maxc - minc);
    myexactlog(63, rangec);
    var v = maxc;
    myexactlog(64, v);
    if (minc == maxc) {
        myexactlog(65, 14);
        myexactlog(66, 0.0, 0.0, v);
        return [0.0, 0.0, v];
    }
    var s = rangec / maxc;
    myexactlog(67, s);
    var rc = (maxc - r) / rangec;
    myexactlog(68, rc);
    var gc = (maxc - g) / rangec;
    myexactlog(69, gc);
    var bc = (maxc - b) / rangec;
    myexactlog(70, bc);
    var h = 1.0;
    myexactlog(71, h);
    if (r == maxc) {
        myexactlog(72, 15);
        var h = bc - gc;
        myexactlog(73, h);
    } else if (g == maxc) {
        myexactlog(74, 1);
    } else {
        myexactlog(75, 3);
        var h = 4.0 + gc - rc;
        myexactlog(76, h);
    }
    h = (((h / 6.0) % 1.0) + 1.0) % 1.0;
    myexactlog(77, h);
    myexactlog(78, h, s, v);
    return [h, s, v];
}

function hsv_to_rgb(h, s, v, ) {
    if (s == 0.0) {
        myexactlog(79, 16);
    }
    var i = (h * 6.0);
    myexactlog(80, i);
}

function user_assert_almost_equal(a, b, ) {
    if (!(Math.abs(a - b) <= 0.0001)) {
        throw new Error();
    }
    myexactlog(81, true);
    return true;
}

function assert_iter_almost_equal(iter1, iter2, ) {
    for (const [a, b] of iter1.slice(0, Math.min(iter1.length, iter2.length)).map((v, i) => [v, iter2[i]])) {
        myexactlog(82, 0);
        user_assert_almost_equal(a, b);
    }
    myexactlog(83, true);
    return true;
}

function test_assertions() {
    console.log("--- rgb_to_yiq ---");
    var tmp = rgb_to_yiq(0.5, 0.5, 0.5);
    myexactlog(84, tmp);
    var expected = [0.49999999999999994, 2.6090241078691177e-17, 4.940492459581946e-17];
    myexactlog(85, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_yiq(0, 0.5, 1);
    myexactlog(86, tmp);
    var expected = [0.40499999999999997, -0.46035, 0.04954999999999998];
    myexactlog(87, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_yiq(1, 0, 0);
    myexactlog(88, tmp);
    var expected = [0.3, 0.599, 0.21299999999999997];
    myexactlog(89, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_yiq(0, 0, 0);
    myexactlog(90, tmp);
    var expected = [0.0, 0.0, 0.0];
    myexactlog(91, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_yiq(1, 0.1, 0.3);
    myexactlog(92, tmp);
    var expected = [0.392, 0.47476, 0.25411999999999996];
    myexactlog(93, expected);
    assert_iter_almost_equal(tmp, expected);
    console.log("--- yiq_to_rgb ---");
    var tmp = yiq_to_rgb(1.0, 0.5957, 0.0);
    myexactlog(94, tmp);
    var expected = [1.0, 0.8363089990996986, 0.33963972286374133];
    myexactlog(95, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = yiq_to_rgb(0.0, -0.5957, -0.5226);
    myexactlog(96, tmp);
    var expected = [0.0, 0.49590315888362624, 0.0];
    myexactlog(97, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = yiq_to_rgb(0.8, 0.1, 0.2);
    myexactlog(98, tmp);
    var expected = [1.0, 0.6453830195326262, 1.0];
    myexactlog(99, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = yiq_to_rgb(0.0, 0.0, 0.0);
    myexactlog(100, tmp);
    var expected = [0.0, 0.0, 0.0];
    myexactlog(101, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = yiq_to_rgb(1.0, 0.0, 0.0);
    myexactlog(102, tmp);
    var expected = [1.0, 1.0, 1.0];
    myexactlog(103, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = yiq_to_rgb(0.5, 0.0, 0.0);
    myexactlog(104, tmp);
    var expected = [0.5, 0.5, 0.5];
    myexactlog(105, expected);
    assert_iter_almost_equal(tmp, expected);
    console.log("--- rgb_to_hls ---");
    var tmp = rgb_to_hls(0.5, 0.5, 0.5);
    myexactlog(106, tmp);
    var expected = [0.0, 0.5, 0.0];
    myexactlog(107, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hls(0, 0.5, 1);
    myexactlog(108, tmp);
    var expected = [0.5833333333333334, 0.5, 1.0];
    myexactlog(109, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hls(1, 0, 0);
    myexactlog(110, tmp);
    var expected = [0.0, 0.5, 1.0];
    myexactlog(111, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hls(0, 0, 0);
    myexactlog(112, tmp);
    var expected = [0.0, 0.0, 0.0];
    myexactlog(113, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hls(1, 0.1, 0.3);
    myexactlog(114, tmp);
    var expected = [0.9629629629629629, 0.55, 1.0000000000000002];
    myexactlog(115, expected);
    assert_iter_almost_equal(tmp, expected);
    console.log("--- hls_to_rgb ---");
    var tmp = hls_to_rgb(0.5, 0.5, 0.5);
    myexactlog(116, tmp);
    var expected = [0.25, 0.7499999999999999, 0.75];
    myexactlog(117, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = hls_to_rgb(0, 0.5, 1);
    myexactlog(118, tmp);
    var expected = [1.0, 0.0, 0.0];
    myexactlog(119, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = hls_to_rgb(1, 0, 0);
    myexactlog(120, tmp);
    var expected = [0, 0, 0];
    myexactlog(121, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = hls_to_rgb(0, 0, 0);
    myexactlog(122, tmp);
    var expected = [0, 0, 0];
    myexactlog(123, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = hls_to_rgb(1, 0.1, 0.3);
    myexactlog(124, tmp);
    var expected = [0.13, 0.07, 0.07];
    myexactlog(125, expected);
    assert_iter_almost_equal(tmp, expected);
    console.log("--- rgb_to_hsv ---");
    var tmp = rgb_to_hsv(0.5, 0.5, 0.5);
    myexactlog(126, tmp);
    var expected = [0.0, 0.0, 0.5];
    myexactlog(127, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hsv(0, 0.5, 1);
    myexactlog(128, tmp);
    var expected = [0.5833333333333334, 1.0, 1];
    myexactlog(129, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hsv(1, 0, 0);
    myexactlog(130, tmp);
    var expected = [0.0, 1.0, 1];
    myexactlog(131, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hsv(0, 0, 0);
    myexactlog(132, tmp);
    var expected = [0.0, 0.0, 0];
    myexactlog(133, expected);
    assert_iter_almost_equal(tmp, expected);
    var tmp = rgb_to_hsv(1, 0.1, 0.3);
    myexactlog(134, tmp);
    var expected = [0.9629629629629629, 0.9, 1];
    myexactlog(135, expected);
    assert_iter_almost_equal(tmp, expected);
    console.log("--- hsv_to_rgb ---");
    var tmp = hsv_to_rgb(0.5, 0.5, 0.5);
    myexactlog(136, tmp);
}

function test() {
    test_assertions();
}

function additional_tests() {}
var ONE_THIRD = 1.0 / 3.0;
myexactlog(137, ONE_THIRD);
var ONE_SIXTH = 1.0 / 6.0;
myexactlog(138, ONE_SIXTH);
var TWO_THIRD = 2.0 / 3.0;
myexactlog(139, TWO_THIRD);
test();