import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Prints the slow instances (taking more than 60 seconds) and plots statistics for each model.
def plot_stats(models):
    global_df = pd.DataFrame(columns=["model", "rectangles", "time", "failures", "restarts"], dtype="int64")
    for model, problems in models.items():
        df = pd.DataFrame(problems)
        stats = df.drop(["x", "y", "w", "h"], axis=1)
        stats["model"] = model
        global_df = global_df.append(stats)

        slow_instances = stats[stats["time"] > 60]

        print("Analyzing {}...".format(model))

        print("Slow instances:")
        for i, row in slow_instances.iterrows():
            print(row)

        print("Plotting graphs related to {} performance.".format(model))
        fig, ax = plt.subplots(1, 2)
        sns.lineplot(x="rectangles", y="time", data=stats, ci=None, ax=ax[0])
        sns.lineplot(x="area", y="time", data=stats, ci=None, ax=ax[1])
        plt.show()
        fig, ax = plt.subplots(1, 2)
        sns.lineplot(x="rectangles", y="failures", data=stats, ci=None, ax=ax[0])
        sns.lineplot(x="area", y="failures", data=stats, ci=None, ax=ax[1])
        plt.show()
        fig, ax = plt.subplots(1, 2)
        sns.lineplot(x="rectangles", y="restarts", data=stats, ci=None, ax=ax[0]) #NOTE: the Chuffed solver doesn't store restart statistics, so this will always be 0.
        sns.lineplot(x="area", y="restarts", data=stats, ci=None, ax=ax[1])
        plt.show()

    print("Plotting global graphs (wrt rectangles).")
    sns.lineplot(x="rectangles", y="time", data=global_df, hue="model", ci=None)
    plt.show()
    sns.lineplot(x="rectangles", y="failures", data=global_df, hue="model", ci=None)
    plt.show()
    sns.lineplot(x="rectangles", y="restarts", data=global_df, hue="model", ci=None)
    plt.show()