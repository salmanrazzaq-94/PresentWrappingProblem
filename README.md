# PresentWrappingProblem
Modelling and Solving the Present Wrapping Problem with CSP (minizinc) and SAT/SMT


To run:
 
Output files are located in CSP/Outputs and SMT/Outputs subfolders (one for each proposed model/encoding).

In order to run the code z3-solver is required, along with a Minizinc command line executable.
Optional dependencies are pandas and seaborn, for plotting performance graphs (to avoid them, comment p.plot_stats(successful) in both CSP_utils/main_CSP.py and SMT/main_SMT.py).
The code was tested with Python 3.7 on JetBrains PyCharm.

All the required configurations (Minizinc.exe path and various directories for instances, logs, etc.) are stored in main.py.

The program will restore execution skipping all the instances already processed and evaluate almost all the models proposed in the attached report, for CSP, SMT and SAT.
This archive contains all the instances already processed: if run as-is, it will print the final report and plot the statistics, in order to restart from scratch, either pass resume=False in main.py or delete Logs and Outputs folders from CSP and SMT.

Single models located in the CSP subfolder can be manually run using Minizinc IDE, each model contains a comment with the suggested solver to use.
In order to use the mzc solution checker files from the IDE, they must be renamed in the same way as the model file (eg. rename Checker.mzc to Diffn model.mzc when running Diffn model.mzn), this is not required for command line execution.

The SMT and SAT models are located in SMT/smt_model.py.
