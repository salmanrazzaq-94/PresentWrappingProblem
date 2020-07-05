% Constants: 
int: n_rects; % Number of rectangles.
int: paper_w; % Width of the strip of paper.
int: paper_h; % Height of the strip of paper.
set of int: NRECTS = 1..n_rects; % Alias for array boundaries.
array[NRECTS] of int: w; % Widths of each rectangle.
array[NRECTS] of int: h; % Heights of each rectangle.

% Variables:
array[NRECTS] of var 0..paper_w: x;
array[NRECTS] of var 0..paper_h: y;

% Constraints:
% 1. Each rectangle must fit inside the paper.
constraint forall (i in NRECTS)(x[i] + w[i] <= paper_w);
constraint forall (i in NRECTS)(y[i] + h[i] <= paper_h);

% 2. No rectangle can overlap.
constraint forall (i, j in NRECTS)((i < j) -> ((not(x[i] <= x[j] /\ x[j] < x[i] + w[i]) /\ not(x[j] <= x[i] /\ x[i] < x[j] + w[j])) \/ (not(y[i] <= y[j] /\ y[j] < y[i] + h[i]) /\ not(y[j] <= y[i] /\ y[i] < y[j] + h[j]))));

% 3. Implied constraint. All rectangles overlapping in one direction must remain inside the paper according to the other direction.
constraint forall (i in NRECTS)(sum(j in NRECTS where i < j /\ x[i] < x[j] /\ x[j] < x[i] + w[i])(h[j]) <= paper_h);
constraint forall (i in NRECTS)(sum(j in NRECTS where i < j /\  y[i] < y[j] /\ y[j] < y[i] + h[i])(w[j]) <= paper_w);

solve
% :: restart_luby(200) % Overridden by Chuffed's restart strategy.
% :: int_search(x ++ y, dom_w_deg, indomain_random) % Not implemented by Chuffed.
satisfy;
output ["x = \(x)\ny = \(y)\nw = \(w)\nh = \(h)\n"];

% Solve using Chuffed. The default settings and search heuristics proved to be good, although a -O5 optimization level is suggested.
% NOTE: for command line execution, apparently solution checking is NOT performed for optimizations above -O1.