import os
import io

# Load each instance file into a ready to use list of instances.
def create_instances(instance_dir):
    instances = []
    for file in os.listdir(instance_dir):
        lines = io.open("{}/{}".format(instance_dir, file)).read().split("\n")
        size = lines[0].split(" ")
        n_rect = int(lines[1])
        rects = []
        for l in lines[2:2 + n_rect]:
            rects.append(l.split(" "))
        w, h = zip(*rects)
        instances.append({"name": file.replace(".txt", ""), "paper_w": size[0], "paper_h": size[1], "n_rects": len(rects), "w": w, "h": h})
    return instances