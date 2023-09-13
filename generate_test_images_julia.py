import os
import numpy as np
import imageio # Only required for generating the gif
from fractal_generator import FractalGenerator
from pygifsicle import optimize
import random

# Define the folder for outputting fractal images
output_dir = "images"
gif_dir = "testgifs_julia"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(gif_dir):
    os.makedirs(gif_dir)


numTestImages = 5

for n in range(0, numTestImages, 1):

    aMin = 0.713
    aMax = 0.714
    a = random.uniform(aMin, aMax)

    bMin = 0.238
    bMax = 0.239
    b = random.uniform(bMin, bMax)

    rMin = 0.012
    rMax = 0.015
    r = random.uniform(rMin, rMax)

    #a, b, r = -0.33, 0.01, 0.1

    r1 = random.uniform(0, 2)
    r2 = random.uniform(0, 2)
    r3 = random.uniform(0, 2)

    b1 = random.uniform(1, 5)
    b2 = random.uniform(1, 5)
    b3 = random.uniform(1, 5)



    total_frames = 10 # Make this smaller if you don't want it to take so long!
    total_time = 1
    images = []
    for i in range(0, total_frames, 1):
        m = FractalGenerator()
        m.set_grid(start_x=-1.7, end_x=1.7,
                start_y=-1.7, end_y=1.7,
                resolution_x=350, resolution_y=350,
                threshold=2.9)
        # Use the periodicity in c to generate a looping gif
        theta = 2 * i * np.pi / total_frames
        c = -(a - r * np.cos(theta)) - (b + r * np.sin(theta)) * 1j
        m.generate_julia(iterations=300, c=c)
        im = m.get_coloured_grid(r1, r2, r3, b1=b1, b2=b2, b3=b3)
        im = im.rotate(90, expand=1)
        images.append(np.array(im))


    # Write out our gif
    fname = "img_" + str(a) + "_" + str(b) + "_" + str(r) + "_" + str(r1) + "_" + str(r2) + "_" + str(r3) + "_" + str(b1) + "_" + str(b2) + "_" + str(b3) + ".gif"
    filename = os.path.join(gif_dir, fname)
    imageio.mimsave(filename, images,'GIF',
                    duration=total_time/total_frames)

    # optimize the gif
    optimize(filename)


    print(filename)