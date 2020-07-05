include "diffn.mzn";
include "cumulative.mzn";
include "geost.mzn";

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
% 1. Allow rotations:
constraint forall (i in NRECTS)(rot_1[i] = w[i] /\ rot_2[i] = h[i] \/ rot_1[i] = h[i] /\ rot_2[i] = w[i]);

% 2. Each rectangle must fit inside the paper. These will be enforced by model 2.
% constraint forall (i in NRECTS)(x[i] + rot_1[i] <= paper_w);
% constraint forall (i in NRECTS)(y[i] + rot_2[i] <= paper_h);

% 3. No rectangle can overlap.
constraint diffn(x, y, rot_1, rot_2);

% 4. Implied constraint. All rectangles overlapping in one direction must remain inside the paper according to the other direction.
% This can be seen as a scheduling metaphor: "Given a set of tasks with starting time x and w, make sure that resource h never exceeds the limit paper_h" (or viceversa).
constraint cumulative(x, rot_1, rot_2, paper_h);
constraint cumulative(y, rot_2, rot_1, paper_w);

% Model 2: geost_bb global constraint.
% Variables:
array[NRECTS, 1..2] of var 0..max(paper_w, paper_h): pos; % 2D array equivalent to x, y.
array[NRECTS] of var 1..2*n_rects: rotation;

% Constraint:
% 1. Fit shapes composed of single rectangles inside a bounding box, with no overlapping.
constraint geost_bb(
  2,
  array2d(1..2*n_rects, 1..2, [if i mod 4 = 0 \/ i mod 4 = 1 then w[(i-1) div 4 + 1] else h[(i-1) div 4 + 1] endif | i in 1..4*n_rects]),
  array2d(1..2*n_rects, 1..2, [0 | i in 1..4*n_rects]),
  [{i} | i in 1..2*n_rects],
  pos,
  rotation,
  [0, 0],
  [paper_w, paper_h]);

% 2. Channeling constraint. Force the first dimension of pos to be x and the second to be y.
constraint forall (i in NRECTS)(x[i] = pos[i,1] /\ y[i] = pos[i,2]);

% % 3. Channeling constraint. Allow rotations on geost model, but force them to be coherent with rotations on diffn model.
constraint forall (i in NRECTS) (rotation[i] = if rot_1[i] = w[i] then 2*i - 1 else 2*i endif);


solve :: restart_luby(200)
:: seq_search([
  int_search(rot_1, first_fail, indomain),
  int_search(pos, dom_w_deg, indomain)
]) satisfy;
output ["x = \(x)\ny = \(y)\nw = \(rot_1)\nh = \(rot_2)\n"];

% Solve using Gecode (Chuffed tends to crash on some inputs, due to out of memory errors, Gecode still requires a lot of memory (eg. more than 10Gb for 38x38), but can succeed with slightly more instances than Chuffed).
% NOTE: for command line execution, apparently solution checking is NOT performed for optimizations above -O1.