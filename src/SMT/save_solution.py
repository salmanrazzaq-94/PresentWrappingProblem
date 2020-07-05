import os
import io

# Save a solution in its wxh out.txt file.
def save_solution(output_dir, solution):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    out = "{}/{}".format(output_dir, solution["name"] + " out.txt")
    wh = solution["name"].split("x")
    with io.open(out, "w+") as output_file:
        output_file.write("{} {}\n".format(wh[0], wh[1]))
        output_file.write("{}\n".format(len(solution["x"])))
        for j in range(len(solution["x"])):
            output_file.write("{} {} {} {}\n".format(solution["x"][j], solution["y"][j], solution["w"][j], solution["h"][j]))