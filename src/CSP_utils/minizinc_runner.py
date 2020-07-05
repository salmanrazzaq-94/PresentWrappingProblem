import os
import io

# Runs Minizinc (using the Chuffed solver) for each model and each instance and saves outputs in the log directory.
# Note: Apparently with an higher optimization the solution checker doesn't work on the command line, therefore here it's set to -O1 (while on the Minizinc IDE it can be set to -O5).
def run_minizinc(minizinc_path, working_dir, models, data_dir, checkers, log_dir, timeout, resume=False):
    flags = " --solver Chuffed --solver-statistics -O1 --time-limit {}".format(timeout * 1000)  # file.mzn -d data.dzn -o output.log
    for i in range(len(models)):
        for file in os.listdir(working_dir + "/" + data_dir):
            path = r"{}/{}/{}".format(working_dir, data_dir, file)
            log = r"{}/{}/{}/{}".format(working_dir, log_dir, models[i].replace(".mzn", ""), file.replace(".dzn", ".log"))

            if not os.path.exists(r"{}/{}/{}".format(working_dir, log_dir, models[i].replace(".mzn", ""))):
                os.makedirs(r"{}/{}/{}".format(working_dir, log_dir, models[i].replace(".mzn", "")))

            if resume and os.path.isfile(log) and os.stat(log).st_size > 0:
                print("File {} already exists. Skipping.".format(log))
            else:
                print("Processing {} using model {} ({} seconds timeout)...".format(path, models[i], timeout))
                cmd = r'"{}" {} "{}/{}" "{}/{}" -d "{}" -o "{}"'.format(minizinc_path, flags, working_dir, models[i], working_dir, checkers[i], path, log)
                out = os.popen(cmd).read()
                print(out)
                with io.open(log, "a+") as l:
                    l.write(out)
    print("Done.")