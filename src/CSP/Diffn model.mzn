include "diffn.mzn";
include "cumulative.mzn";

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
constraint diffn(x, y, w, h);

% 3. Implied constraint. All rectangles overlapping in one direction must remain inside the paper according to the other direction.
% This can be seen as a scheduling metaphor: "Given a set of tasks with starting time x and duration w, make sure that resource h never exceeds the limit paper_h" (or viceversa).
constraint cumulative(x, w, h, paper_h);
constraint cumulative(y, h, w, paper_w);

solve satisfy;
output ["x = \(x)\ny = \(y)\nw = \(w)\nh = \(h)\n"];

% Solve using Chuffed. The default settings and search heuristics proved to be good, although a -O5 optimization level is suggested.
% NOTE: for command line execution, apparently solution checking is NOT performed for optimizations above -O1.