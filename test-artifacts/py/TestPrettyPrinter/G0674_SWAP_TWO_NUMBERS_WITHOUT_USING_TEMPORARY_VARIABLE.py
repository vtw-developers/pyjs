def f_gold(xp, yp):
    xp[0] = xp[0] ^ yp[0]
    yp[0] = xp[0] ^ yp[0]
    xp[0] = xp[0] ^ yp[0]