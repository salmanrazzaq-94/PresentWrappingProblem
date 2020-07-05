import os
import io

# For each instance file, create a dzn data file.
def create_instances(working_dir, instance_dir, data_dir):
    if not os.path.exists(r"{}/{}".format(working_dir, data_dir)):
        os.makedirs(r"{}/{}".format(working_dir, data_dir))

    for file in os.listdir("{}/{}".format(working_dir, instance_dir)):
        lines = io.open("{}/{}/{}".format(working_dir, instance_dir, file)).read().split("\n")
        size = lines[0].split(" ")
        n_rect = int(lines[1])
        rect = []
        for l in lines[2:2 + n_rect]:
            rect.append(l.split(" "))

        _create_model(size, rect, "{}/{}/{}".format(working_dir, data_dir, file.replace(".txt", ".dzn")))

# Write a single instance to a dzn file.
def _create_model(size, rect, filename):
    with io.open(filename, "w+") as file:
        file.write("n_rects = {};\n".format(len(rect)))
        file.write("paper_w = {};\n".format(size[0]))
        file.write("paper_h = {};\n".format(size[1]))
        ws = ", ".join([r[0] for r in rect])
        hs = ", ".join([r[1] for r in rect])
        file.write("w = [" + ws + "];\n")
        file.write("h = [" + hs + "];\n")