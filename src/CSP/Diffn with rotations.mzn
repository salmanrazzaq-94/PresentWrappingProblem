include "diffn.mzn";
include "cumulative.mzn";

% Constants: 
int: n_rects; % Number of rectangles.
int: paper_w; % Width of the strip of paper.
int: paper_h; % Height of the strip of paper.
set of int: NRECTS = 1..n_rects; % Alias for array boundaries.
array[NRECTS] of int: w; % Widths of each rectangle.
array[NRECTS] of int: h; % Heights of each rectangle.


% Model 1: diffn global constraint.
% Variables:
array[NRECTS] of var 0..paper_w: x;
array[NRECTS] of var 0..paper_h: y;

array[NRECTS] of var 0..max(paper_w, paper_h): rot_1; % Width after rotation.
array[NRECTS] of var 0..max(paper_w, paper_h): rot_2; % Height dimension after rotation.

% Constraints:
% 1. Allow rotations.
constraint forall (i in NRECTS)(rot_1[i] = w[i] /\ rot_2[i] = h[i] \/ rot_1[i] = h[i] /\ rot_2[i] = w[i]);

% 2. Each rectangle must fit inside the paper.
constraint forall (i in NRECTS)(x[i] + rot_1[i] <= paper_w);
constraint forall (i in NRECTS)(y[i] + rot_2[i] <= paper_h);

% 3. No rectangle can overlap.
constraint diffn(x, y, rot_1, rot_2);

% 4. Implied constraint. All rectangles overlapping in one direction must remain inside the paper according to the other direction.
% This can be seen as a scheduling metaphor: "Given a set of tasks with starting time x and w, make sure that resource h never exceeds the limit paper_h" (or viceversa).
constraint cumulative(x, rot_1, rot_2, paper_h);
constraint cumulative(y, rot_2, rot_1, paper_w);

solve satisfy;
output ["x = \(x)\ny = \(y)\nw = \(rot_1)\nh = \(rot_2)\n"];

% Solve using Chuffed. The default settings and search heuristics proved to be good, although a -O5 optimization level is suggested.
% NOTE: for command line execution, apparently solution checking is NOT performed for optimizations above -O1.