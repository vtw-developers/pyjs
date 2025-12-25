def rgb_to_yiq(r, g, b):
    y = 0.30 * r + 0.59 * g + 0.11 * b
    myexactlog(1, y)
    i = 0.74 * (r - y) - 0.27 * (b - y)
    myexactlog(2, i)
    q = 0.48 * (r - y) + 0.41 * (b - y)
    myexactlog(3, q)
    myexactlog(4, (y, i, q))
    return (y, i, q)
def yiq_to_rgb(y, i, q):
    r = y + 0.9468822170900693 * i + 0.6235565819861433 * q
    myexactlog(5, r)
    g = y - 0.27478764629897834 * i - 0.6356910791873801 * q
    myexactlog(6, g)
    b = y - 1.1085450346420322 * i + 1.7090069284064666 * q
    myexactlog(7, b)
    if r < 0.0:
        myexactlog(8, 0)
        r = 0.0
        myexactlog(9, r)
    if g < 0.0:
        myexactlog(10, 1)
        pass
    if b < 0.0:
        myexactlog(11, 2)
        b = 0.0
        myexactlog(12, b)
    if r > 1.0:
        myexactlog(13, 3)
        r = 1.0
        myexactlog(14, r)
    if g > 1.0:
        myexactlog(15, 4)
        pass
    if b > 1.0:
        myexactlog(16, 5)
        b = 1.0
        myexactlog(17, b)
    myexactlog(18, [r, g, b])
    return [r, g, b]
def rgb_to_hls(r, g, b):
    maxc = max(r, g, b)
    myexactlog(19, maxc)
    minc = min(r, g, b)
    myexactlog(20, minc)
    sumc = (maxc + minc)
    myexactlog(21, sumc)
    rangec = (maxc - minc)
    myexactlog(22, rangec)
    l = sumc / 2.0
    myexactlog(23, l)
    if minc == maxc:
        myexactlog(24, 6)
        myexactlog(25, 0.0, l, 0.0)
        return 0.0, l, 0.0
    s = 1.0
    myexactlog(26, s)
    if l <= 0.5:
        myexactlog(27, 7)
        s = rangec / sumc
        myexactlog(28, s)
    else:
        myexactlog(29, 0)
        s = rangec / (2.0 - sumc)
        myexactlog(30, s)
    rc = (maxc - r) / rangec
    myexactlog(31, rc)
    gc = (maxc - g) / rangec
    myexactlog(32, gc)
    bc = (maxc - b) / rangec
    myexactlog(33, bc)
    h = 1.0
    myexactlog(34, h)
    if r == maxc:
        myexactlog(35, 8)
        h = bc - gc
        myexactlog(36, h)
    elif g == maxc:
        myexactlog(37, 0)
        pass
    else:
        myexactlog(38, 1)
        h = 4.0 + gc - rc
        myexactlog(39, h)
    h = (h / 6.0) % 1.0
    myexactlog(40, h)
    myexactlog(41, h, l, s)
    return h, l, s
def hls_to_rgb(h, l, s):
    if s == 0.0:
        myexactlog(42, 9)
        pass
    m2 = 0.0
    myexactlog(43, m2)
    if l <= 0.5:
        myexactlog(44, 10)
        m2 = l * (1.0 + s)
        myexactlog(45, m2)
    else:
        myexactlog(46, 2)
        pass
    m1 = 2.0 * l - m2
    myexactlog(47, m1)
    tmp_1 = _v(m1, m2, h + ONE_THIRD)
    myexactlog(48, tmp_1)
    tmp_2 = _v(m1, m2, h)
    myexactlog(49, tmp_2)
    tmp_3 = _v(m1, m2, h - ONE_THIRD)
    myexactlog(50, tmp_3)
def _v(m1, m2, hue):
    hue = hue % 1.0
    myexactlog(51, hue)
    if hue < ONE_SIXTH:
        myexactlog(52, 11)
        pass
    if hue < 0.5:
        myexactlog(53, 12)
        myexactlog(54, m2)
        return m2
    if hue < TWO_THIRD:
        myexactlog(55, 13)
        myexactlog(56, m1 + (m2 - m1) * (TWO_THIRD - hue) * 6.0)
        return m1 + (m2 - m1) * (TWO_THIRD - hue) * 6.0
    myexactlog(57, m1)
    return m1
def rgb_to_hsv(r, g, b):
    pass
def hsv_to_rgb(h, s, v):
    pass
def user_assert_almost_equal(a, b):
    assert (abs(a - b) <= 0.0001)
    myexactlog(58, True)
    return True
def assert_iter_almost_equal(iter1, iter2):
    for a, b in zip(iter1, iter2):
        myexactlog(59, 0)
        user_assert_almost_equal(a, b)
    myexactlog(60, True)
    return True
def test_assertions():
    print("--- rgb_to_yiq ---")
    tmp = rgb_to_yiq(0.5, 0.5, 0.5)
    myexactlog(61, tmp)
    expected = [0.49999999999999994, 2.6090241078691177e-17, 4.940492459581946e-17]
    myexactlog(62, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_yiq(0, 0.5, 1)
    myexactlog(63, tmp)
    expected = [0.40499999999999997, -0.46035, 0.04954999999999998]
    myexactlog(64, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_yiq(1, 0, 0)
    myexactlog(65, tmp)
    expected = [0.3, 0.599, 0.21299999999999997]
    myexactlog(66, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_yiq(0, 0, 0)
    myexactlog(67, tmp)
    expected = [0.0, 0.0, 0.0]
    myexactlog(68, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_yiq(1, 0.1, 0.3)
    myexactlog(69, tmp)
    expected = [0.392, 0.47476, 0.25411999999999996]
    myexactlog(70, expected)
    assert_iter_almost_equal(tmp, expected)
    print("--- yiq_to_rgb ---")
    tmp = yiq_to_rgb(1.0, 0.5957, 0.0)
    myexactlog(71, tmp)
    expected = [1.0, 0.8363089990996986, 0.33963972286374133]
    myexactlog(72, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = yiq_to_rgb(0.0, -0.5957, -0.5226)
    myexactlog(73, tmp)
    expected = [0.0, 0.49590315888362624, 0.0]
    myexactlog(74, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = yiq_to_rgb(0.8, 0.1, 0.2)
    myexactlog(75, tmp)
    expected = [1.0, 0.6453830195326262, 1.0]
    myexactlog(76, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = yiq_to_rgb(0.0, 0.0, 0.0)
    myexactlog(77, tmp)
    expected = [0.0, 0.0, 0.0]
    myexactlog(78, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = yiq_to_rgb(1.0, 0.0, 0.0)
    myexactlog(79, tmp)
    expected = [1.0, 1.0, 1.0]
    myexactlog(80, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = yiq_to_rgb(0.5, 0.0, 0.0)
    myexactlog(81, tmp)
    expected = [0.5, 0.5, 0.5]
    myexactlog(82, expected)
    assert_iter_almost_equal(tmp, expected)
    print("--- rgb_to_hls ---")
    tmp = rgb_to_hls(0.5, 0.5, 0.5)
    myexactlog(83, tmp)
    expected = [0.0, 0.5, 0.0]
    myexactlog(84, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_hls(0, 0.5, 1)
    myexactlog(85, tmp)
    expected = [0.5833333333333334, 0.5, 1.0]
    myexactlog(86, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_hls(1, 0, 0)
    myexactlog(87, tmp)
    expected = [0.0, 0.5, 1.0]
    myexactlog(88, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_hls(0, 0, 0)
    myexactlog(89, tmp)
    expected = [0.0, 0.0, 0.0]
    myexactlog(90, expected)
    assert_iter_almost_equal(tmp, expected)
    tmp = rgb_to_hls(1, 0.1, 0.3)
    myexactlog(91, tmp)
    expected = [0.9629629629629629, 0.55, 1.0000000000000002]
    myexactlog(92, expected)
    assert_iter_almost_equal(tmp, expected)
    print("--- hls_to_rgb ---")
    tmp = hls_to_rgb(0.5, 0.5, 0.5)
    myexactlog(93, tmp)
def test():
    test_assertions()
def additional_tests():
    pass
ONE_THIRD = 1.0 / 3.0
myexactlog(94, ONE_THIRD)
ONE_SIXTH = 1.0 / 6.0
myexactlog(95, ONE_SIXTH)
TWO_THIRD = 2.0 / 3.0
myexactlog(96, TWO_THIRD)
test()