import os
import numpy as np
import imageio # Only required for generating the gif
from fractal_generator import FractalGenerator
from pygifsicle import optimize
import random

# Define the folder for outputting fractal images
output_dir = "images"
gif_dir = "testgifs_mandlebrot"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(gif_dir):
    os.makedirs(gif_dir)


numTestImages = 5

for n in range(0, numTestImages, 1):

    
    aMin = -2
    aMax = 0.75
    a = random.uniform(aMin, aMax)

    bMin = -1
    bMax = 1
    b = random.uniform(bMin, bMax)

    wMin = 0.001
    wMax = 0.01
    w = random.uniform(wMin, wMax)


    # for mandlebrot, this is our "zoom"
    zMin = 0.5
    zMax = 0.9
    z = random.uniform(zMin, zMax)

    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)
    r3 = random.uniform(0, 1)

    b1 = random.uniform(1, 3)
    b2 = random.uniform(1, 3)
    b3 = random.uniform(1, 3)

    total_frames = 5 # Make this smaller if you don't want it to take so long!
    total_time = 1
    images = []
    fname = "img_" + str(a) + "_" + str(b) + "_" + str(z) + "_" + str(r1) + "_" + str(r2) + "_" + str(r3) + "_" + str(b1) + "_" + str(b2) + "_" + str(b3) + ".gif"

    print("generating" + fname)

    for i in range(0, total_frames, 1):
        m = FractalGenerator()


        zoom_factor = 1 - (z * i / total_frames)
        start_y = (b - w) * zoom_factor
        end_y = (b + w) * zoom_factor
        start_x = (a - w) * zoom_factor
        end_x = (a + w) * zoom_factor
        
        print("z=" + str(z))
        print("w=" + str(w))
        print("a=" + str(a))
        print("b=" + str(b))
        print("start_x=" + str(start_x))
        print("end_x=" + str(end_x))
        print("start_y=" + str(start_y))
        print("end_y=" + str(end_y))
        


        m.set_grid(start_x=start_x, end_x=end_x,
                start_y=start_y, end_y=end_y,
                resolution_x=350, resolution_y=350,
                threshold=4)
        
        m.generate_mandelbrot(iterations=200)
        im = m.get_coloured_grid(r1, r2, r3, b1=b1, b2=b2, b3=b3)
        #im = im.rotate(90, expand=1)
        images.append(np.array(im))


    # Write out our gif
    
    filename = os.path.join(gif_dir, fname)
    imageio.mimsave(filename, images,'GIF',
                    duration=total_time/total_frames)

    # optimize the gif
    optimize(filename)
