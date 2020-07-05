# Check if a provided solution is valid.
def check(solution):
    if _is_inside_paper(solution) and _no_rectangle_overlaps(solution):
        print("Solution is CORRECT.")
    else:
        print("Solution is INCORRECT.")

# Return True if all the rectangles are inside the paper, otherwise print which aren't.
def _is_inside_paper(solution):
    paper_w = solution["paper_w"]
    paper_h = solution["paper_h"]
    x = solution["x"]
    y = solution["y"]
    w = solution["w"]
    h = solution["h"]

    out = True
    for i in range(len(x)):
        ok = x[i] + w[i] <= paper_w
        ok = ok and y[i] + h[i] <= paper_h
        if ok == False:
            print("Rectangle ({}, {}, {}, {}) is outside the paper.".format(x[i],y[i],w[i],h[i]))
        out = out and ok
    return out

# Return True if no two rectangles overlap, otherwise print the couples that do.
def _no_rectangle_overlaps(solution):
    x = solution["x"]
    y = solution["y"]
    w = solution["w"]
    h = solution["h"]

    out = True
    for i in range(len(x)):
        for j in range(i):
            ok = x[i] + w[i] <= x[j] or x[j] + w[j] <= x[i] or y[i] + h[i] <= y[j] or y[j] + h[j] <= y[i]
            if ok == False:
                print("Rectangles ({}, {}, {}, {}) and ({}, {}, {}, {}) overlap.".format(x[i], y[i], w[i], h[i], x[j], y[j], w[j], h[j]))
            out = out and ok
    return out