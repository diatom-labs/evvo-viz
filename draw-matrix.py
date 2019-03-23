import os
import re
from datetime import datetime

import webbrowser
import numpy as np
from PIL import Image

with open("../evvo/out/matrix.log") as file:
    pareto_frontiers_strings = [group[1] for group in
                                [re.search("(Vector\(.*?\)\))", line)
                                 for line in file if "pareto = " in line]
                                if group]
    pareto_frontier_items = [eval(p.replace("Vector(", "[").replace(")", "]"))
                             for p in pareto_frontiers_strings]

color_map = np.array([
    [255, 255, 255, 255],
    [0, 0, 0, 255],
    [0, 0, 255, 255],
    [255, 0, 0, 255],
    [0, 255, 0, 255],
])

frames = color_map[np.array(pareto_frontier_items)]

size = (frames.shape[2] * 20, frames.shape[1] * 20)
images = [Image.fromarray(frame.astype('uint8'), mode="RGBA").resize(size)
          for frame in frames]
images[-1].show()

name = datetime.now().timestamp()

filename = f"out/matrix{name}.gif"
images[0].save(filename, save_all=True, append_images=images[1:], duration=100, loop=0)

os.system(f"open -a /Applications/Safari.app \"file://{os.path.abspath(filename)}\"")