from CSP_utils import main_CSP as csp
from SMT import main_SMT as smt

timeout = 600 # Timeout (in seconds) for running each instance.

working_dir = "CSP" # Working directory for CSP problems, must contain the models.
data_dir = "Data" # Data directory for CSP problems.
minizinc_path = r"E:/Program Files/MiniZinc/minizinc.exe" # Path of the minizinc command line executable.
log_dir = "Logs" # Directory in which execution logs will be saved.
output_dir = "Outputs" # Directory in which files wxh out.txt will be saved (each model will be saved in its own subdirectory).
instances_dir = "../Instances" # Directory in which the wxh.txt instances are saved (relative to working_dir).

# Run the CSP execution for all models and all instances. If resume is set to True, previously solved instances won't be rerun (even if their outcome was unknown).
csp.run(working_dir, data_dir, instances_dir, log_dir, output_dir, minizinc_path, timeout, resume=True)

working_dir = "SMT" # Working directory for SMT problems, since models are generated at runtime, it will only be used to save outputs.
log_dir = "Logs" # Directory in which execution logs will be saved.
output_dir = "Outputs" # Directory in which files wxh out.txt will be saved (each model will be saved in its own subdirectory).
instances_dir = "../Instances" # Directory in which the wxh.txt instances are saved (relative to working_dir).

# Run the SAT/SMT solving for all models and all instances.
# If resume is set to True, previously solved instances won't be rerun. If retry_unknown is set to True, unknown instances are retried (NOTE: the log file will append a new entry instead of updating the last one).
smt.run(working_dir, instances_dir, log_dir, output_dir, timeout, resume=True, retry_unknown=False)