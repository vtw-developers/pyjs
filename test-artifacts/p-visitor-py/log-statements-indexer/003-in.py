def test():
    "--- test function ---" ;
"-----------------"
def f_gold(XY, n, Xmin, Ymin, Xmax, Ymax):
    print("Point inside the viewing pane:")
    for i in range(n):
        if (XY[i][0] >= Xmin) and (XY[i][0] <= Xmax):
            if (XY[i][1] >= Ymin) and (XY[i][1] <= Ymax):
                print("[", XY[i][0], ", ", XY[i][1], "]", sep="", end="")
    print("\n\nPoint outside the viewing pane:")
    for i in range(n):
        if (XY[i][0] < Xmin) or (XY[i][0] > Xmax):
            print("[", XY[i][0], ", ", XY[i][1], "]", sep="", end="")
        if (XY[i][1] < Ymin) or (XY[i][1] > Ymax):
            print("[", XY[i][0], ", ", XY[i][1], "]", sep="", end="")
"-----------------"
test()
