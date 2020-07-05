from CSP_utils import data_builder as d, minizinc_runner as r, solution_extractor as s, plot_stats as p

# Main file for the CSP execution.

def run(working_dir, data_dir, instances_dir, log_dir, output_dir, minizinc_path, timeout, resume=True):
    # Create the dzn files from the provided instances.
    d.create_instances(working_dir, instances_dir, data_dir)

    # Models to run.
    models = ["Dual.mzn", "Diffn model.mzn", "Geost model.mzn", "Naive model.mzn", "Diffn with rotations.mzn"]
    # Solution checkers related to each model.
    checkers = ["Checker.mzc", "Checker.mzc", "Checker.mzc", "Checker.mzc", "Checker with rotations.mzc"]

    # Run Minizinc for each model on each data file. If resume is False, rerun every instance and overwrite existing logs.
    r.run_minizinc(minizinc_path, working_dir, models, data_dir, checkers, log_dir, timeout, resume=resume)

    # Extract the solutions from the log files and return the set of successful instances.
    [successful, unsatisfiable, unknown] = s.save_solutions(working_dir, models, log_dir, output_dir)

    # For each model, print the unsatisfiable, unknown and successful instances.
    for m in models:
        print("Results for {}".format(m))
        print("Unsatisfiable instances:")
        if len(unsatisfiable[m.replace(".mzn", "")]) == 0:
            print("None.")
        else:
            for u in unsatisfiable[m.replace(".mzn", "")]:
                print(u)
        print("Unknown instances ({} seconds timeout expired):".format(timeout))
        if len(unknown[m.replace(".mzn", "")]) == 0:
            print("None.")
        else:
            for u in unknown[m.replace(".mzn", "")]:
                print(u)
        print("Successful instances:")
        if len(successful[m.replace(".mzn", "")]) == 0:
            print("None.")
        else:
            for succ in successful[m.replace(".mzn", "")]:
                print(succ['name'])

    # Print slow instances and plot statistics, for each model and globally.
    p.plot_stats(successful)