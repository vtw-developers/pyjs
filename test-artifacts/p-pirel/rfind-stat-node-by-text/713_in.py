def f_gold(XY, n, Xmin, Ymin, Xmax, Ymax):
    print("Point inside the viewing pane:")
    for i in range(n):
        myexactlog(1, 0)
        if (XY[i][0] >= Xmin) and (XY[i][0] <= Xmax):
            myexactlog(2, 1)
            if (XY[i][1] >= Ymin) and (XY[i][1] <= Ymax):
                myexactlog(3, 0)
                print("[", XY[i][0], ", ", XY[i][1], "]", sep="", end="")
        break