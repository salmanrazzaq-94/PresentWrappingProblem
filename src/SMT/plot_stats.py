import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_stats(instances):
    global_df = pd.DataFrame(columns=["model", "n_rects", "time"])
    for model, solutions in instances.items():

        df = pd.DataFrame(solutions)
        df["n_rects"] = df["x"].apply(lambda x: len(x))
        df["area"] = df["name"].apply(lambda x: int(x.split("x")[0]) * int(x.split("x")[1]))

        stats = df.drop(["x", "y", "w", "h"], axis=1)
        stats["model"] = model
        global_df = global_df.append(stats)

        slow_instances = stats[stats["time"] > 60]

        print("Slow instances for model {}:".format(model))
        if len(slow_instances) == 0:
            print("None.")
        else:
            for i, row in slow_instances.iterrows():
                print(row)

        print("Plotting graphs related to {} performance.".format(model))
        fig, ax = plt.subplots(1, 2)
        sns.lineplot(x="n_rects", y="time", data=stats, ci=None, ax=ax[0])
        sns.lineplot(x="area", y="time", data=stats, ci=None, ax=ax[1])
        plt.show()
    print("Plotting global graph (time wrt n_rects).")
    sns.lineplot(x="n_rects", y="time", data=global_df, hue="model", ci=None)
    plt.show()