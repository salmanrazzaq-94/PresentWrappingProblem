import z3
import time

# SMT/SAT solver file.

# Solve the provided instance using the desired configurations (which will determine the model used), profile its execution time and extracts the solution in a readable format.
def solve(instance, timeout, implied_constraints=False, rotations=False, use_sat=False):
    if use_sat:
        solver, variables = _create_sat_solver(instance)
    else:
        solver, variables = _create_smt_solver(instance, implied_constraints, rotations)
    solver.set("timeout", timeout * 1000)
    start = time.time()
    outcome = solver.check()
    stop = time.time()
    solving_time = stop - start

    if outcome == z3.sat:
        m = solver.model()
        if use_sat:
            w = [int(w) for w in instance["w"]]
            h = [int(h) for h in instance["h"]]
            x = [[m.evaluate(variables["x"][i][j]) for j in range(int(instance["paper_w"]))].index(True) for i in range(int(instance["n_rects"]))]
            y = [[m.evaluate(variables["y"][i][j]) for j in range(int(instance["paper_h"]))].index(True) for i in range(int(instance["n_rects"]))]
        else:
            x = [m.evaluate(variables["x"][i]).as_long() for i in range(instance["n_rects"])]
            y = [m.evaluate(variables["y"][i]).as_long() for i in range(instance["n_rects"])]
            w = [m.evaluate(variables["w"][i]).as_long() for i in range(instance["n_rects"])]
            h = [m.evaluate(variables["h"][i]).as_long() for i in range(instance["n_rects"])]
        return {"name": instance["name"], "time": solving_time, "x": x, "y": y, "w": w, "h": h, "paper_w": int(instance["paper_w"]), "paper_h": int(instance["paper_h"])}
    elif outcome == z3.unsat:
        return "UNSATISFIABLE"
    elif outcome == z3.unknown:
        return "UNKNOWN"

# SMT model, if implied_constraints or rotations are True, add clauses related to them. Returns the solver and a dictionary of variables to query.
def _create_smt_solver(instance, implied_constraints, rotations):
    variables = {}

    # Constants:
    n_rects = int(instance["n_rects"])
    paper_w = int(instance["paper_w"])
    paper_h = int(instance["paper_h"])
    w = instance["w"]
    h = instance["h"]

    # Variables:
    w_i = [z3.Int('w_%s' % i) for i in range(n_rects)]
    h_i = [z3.Int('h_%s' % i) for i in range(n_rects)]
    x_i = [z3.Int("x_%s" % i) for i in range(paper_w)]
    y_i = [z3.Int("y_%s" % i) for i in range(paper_h)]

    # Constraints:
    # 1. Assign widths and heights:
    rectangle_values = [z3.And(w[i] == w_i[i], h[i] == h_i[i]) for i in range(n_rects)]
    # 2. Rectangles must be inside paper:
    global_boundary = [z3.And(x_i[i] >= 0, x_i[i] + w_i[i] <= paper_w, y_i[i] >= 0, y_i[i] + h_i[i] <= paper_h) for i in range(n_rects)]
    # 3. Rectangles must not overlap:
    overlapping_constraint = [z3.Or(x_i[i] + w_i[i] <= x_i[j], x_i[j] + w_i[j] <= x_i[i], y_i[i] + h_i[i] <= y_i[j], y_i[j] + h_i[j] <= y_i[i]) for j in range(n_rects) for i in range(j)]
    # 4. Implied constraint. sum of crossed rectangles must not exceed the paper.
    implied_1 = [z3.Sum([z3.If(z3.And(x_i[i] < x_i[j], x_i[j] < x_i[i] + w_i[i]), h_i[j], 0) for j in range(i)]) <= paper_h for i in range(n_rects)]
    implied_2 = [z3.Sum([z3.If(z3.And(y_i[i] < y_i[j], y_i[j] < y_i[i] + h_i[i]), w_i[j], 0) for j in range(i)]) <= paper_w for i in range(n_rects)]

    # 5. Allow rotations. Overwrites the previous rectangle_values definition.
    rectangle_values_with_rotations = [z3.Or(z3.And(w[i] == w_i[i], h[i] == h_i[i]), z3.And(h[i] == w_i[i], w[i] == h_i[i])) for i in range(n_rects)]

    s = z3.Solver()
    if rotations:
        s.add(rectangle_values_with_rotations)
    else:
        s.add(rectangle_values)
    s.add(global_boundary)
    s.add(overlapping_constraint)
    if implied_constraints:
        s.add(implied_1)
        s.add(implied_2)

    variables["x"] = x_i
    variables["y"] = y_i
    variables["w"] = w_i
    variables["h"] = h_i

    return s, variables

# SAT model. Returns the solver and a dictionary of variables to query.
def _create_sat_solver(instance):
    variables = {}

    # Constants:
    n_rects = int(instance["n_rects"])
    paper_w = int(instance["paper_w"])
    paper_h = int(instance["paper_h"])
    w = [int(w) for w in instance["w"]]
    h = [int(h) for h in instance["h"]]

    # Variables:
    # Position:
    x_ij = [[z3.Bool("x_{}_{}".format(i, j)) for j in range(paper_w + 1)] for i in range(n_rects)]
    y_ij = [[z3.Bool("y_{}_{}".format(i, j)) for j in range(paper_h + 1)] for i in range(n_rects)]
    # Space occupation:
    r_ijk = [[[z3.Bool("y_{}_{}_{}".format(i, j, k)) for k in range(paper_h + 1)] for j in range(paper_w + 1)] for i in range(n_rects)]

    # Constraints:
    # 1. Each rectangle must have an assigned coordinate.
    assigned = [z3.And(z3.Or([x_ij[i][j] for j in range(paper_w + 1)]), z3.Or([y_ij[i][j] for j in range(paper_h + 1)])) for i in range(n_rects)]

    # 2. Spatial occupation: Each rectangle occupies all "pixels" according to its width/height
    occupation = [z3.And(x_ij[i][j], y_ij[i][k]) == z3.And([r_ijk[i][j + l][k + m] for l in range(w[i]) for m in range(h[i]) if j + l <= paper_w and k + m <= paper_h]) for i in range(n_rects) for j in range(paper_w + 1) for k in range(paper_h + 1)]

    # 3. Rectangles must be inside the paper. >= 0 implicit. Enforcing only < paper_w/paper_h.
    inside_x = [z3.Not(x_ij[i][j]) for i in range(n_rects) for j in range(paper_w + 1) if j + w[i] >= paper_w + 1]
    inside_y = [z3.Not(y_ij[i][j]) for i in range(n_rects) for j in range(paper_h + 1) if j + h[i] >= paper_h + 1]

    # 4. No overlap
    nooverlap = [z3.Implies(r_ijk[i][j][k], z3.Not(z3.Or([r_ijk[l][j][k] for l in range(n_rects) if l != i]))) for i in range(n_rects) for j in range(paper_w + 1) for k in range(paper_h + 1)]

    s = z3.Solver()
    s.add(assigned)
    s.add(inside_x)
    s.add(inside_y)
    s.add(occupation)
    s.add(nooverlap)

    variables["x"] = x_ij
    variables["y"] = y_ij

    return s, variables