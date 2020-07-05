import io
import os
import re

from SMT import create_instances as c, smt_model as sm, solution_checker as ck, save_solution as ss, plot_stats as p

# Main file for SMT/SAT execution.

def run(working_dir, instances_dir, log_dir, output_dir, timeout, resume=True, retry_unknown=False):
    # Four models are SMT (integer variables) and one is SAT (boolean variables).
    models = ["no implied no rotations", "implied no rotations", "no implied rotations", "implied rotations", "SAT no rotations"]
    options = [[False, False, False], [True, False, False], [False, True, False], [True, True, False], [False, False, True]]

    # Creates a list of instances from files.
    instances = c.create_instances(r"{}/{}".format(working_dir, instances_dir))
    successful = {}
    unsatisfiable = {}
    unknown = {}

    for m in range(len(models)):
        print("Using model {}...".format(models[m]))
        successful[models[m]] = []
        unsatisfiable[models[m]] = []
        unknown[models[m]] = []

        if not os.path.exists(r"{}/{}".format(working_dir, log_dir)):
            os.makedirs(r"{}/{}".format(working_dir, log_dir))

        # Save a different execution log for each model. This log will also be used to skip already solved instances.
        with io.open("{}/{}/{}.log".format(working_dir, log_dir, models[m]), "a+") as log_file:
            # Read the log and extract all the previously run solutions.
            if resume:
                log_file.seek(0)
                content = log_file.read().split("\n##########\n")
                instances_done = []
                for instance in content:
                    match = re.search("([0-9]+x[0-9]+): UNSATISFIABLE", instance)
                    if match:
                        unsatisfiable[models[m]].append(match.group(1))
                        instances_done.append(match.group(1))
                    match = re.search("([0-9]+x[0-9]+): UNKNOWN", instance)
                    if match:
                        if not retry_unknown:
                            unknown[models[m]].append(match.group(1))
                            instances_done.append(match.group(1))
                    match = re.search("([0-9]+x[0-9]+): SATISFIABLE\n", instance)
                    if match:
                        name = match.group(1)
                        match2 = re.search("x = \[(.*)\]\n", instance)
                        x = [int(x) for x in match2.group(1).split(", ")]
                        match2 = re.search("y = \[(.*)\]\n", instance)
                        y = [int(y) for y in match2.group(1).split(", ")]
                        match2 = re.search("w = \[(.*)\]\n", instance)
                        w = [int(w) for w in match2.group(1).split(", ")]
                        match2 = re.search("h = \[(.*)\]\n", instance)
                        h = [int(h) for h in match2.group(1).split(", ")]
                        match2 = re.search("time = (.*)", instance)
                        solving_time = float(match2.group(1))
                        successful[models[m]].append({"name": name, "x": x, "y": y, "w": w, "h": h, "time": solving_time})
                        instances_done.append(name)
            else:
                log_file.truncate(0)

            for i in instances:
                if resume and i["name"] in instances_done:
                    print("Instance {} already solved.".format(i["name"]))
                else:
                    print("Solving instance {}...".format(i["name"]))
                    log_file.write("{}: ".format(i["name"]))
                    # Solve the instance on the given model.
                    solution = sm.solve(i, timeout, options[m][0], options[m][1], options[m][2])
                    if solution == "UNKNOWN":
                        unknown[models[m]].append(i["name"])
                        print(solution)
                        log_file.write("UNKNOWN\n##########\n")
                    elif solution == "UNSATISFIABLE":
                        unsatisfiable[models[m]].append(i["name"])
                        print(solution)
                        log_file.write("UNSATISFIABLE\n##########\n")
                    else:
                        successful[models[m]].append(solution)
                        print("x = {}".format(solution["x"]))
                        print("y = {}".format(solution["y"]))
                        print("w = {}".format(solution["w"]))
                        print("h = {}".format(solution["h"]))
                        print("Solving time: {}".format(solution["time"]))

                        log_file.write("SATISFIABLE\nx = {}\ny = {}\nw = {}\nh = {}\ntime = {}\n##########\n".format(solution["x"], solution["y"], solution["w"], solution["h"], solution["time"]))
                        log_file.flush()

                        # Check if the solution found is valid.
                        ck.check(solution)
                        # Save the solution in the wxh out.txt file.
                        ss.save_solution("{}/{}/{}".format(working_dir, output_dir, models[m]), solution)

            # Print the lists of unsatisfiable, unknown and successful instances.
            print("Unsatisfiable instances:")
            if len(unsatisfiable[models[m]]) == 0:
                print("None.")
            else:
                for u in unsatisfiable[models[m]]:
                    print(u)
            print("Unknown instances ({} seconds timeout expired):".format(timeout))
            if len(unknown[models[m]]) == 0:
                print("None.")
            else:
                for u in unknown[models[m]]:
                    print(u)
            print("Satisfiable instances:")
            if len (successful[models[m]]) == 0:
                print("None.")
            else:
                for s in successful[models[m]]:
                    print(s["name"])

    # Print slow instances and plot statistics, for each model and globally.
    p.plot_stats(successful)