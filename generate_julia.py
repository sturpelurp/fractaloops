import os
import numpy as np
import imageio # Only required for generating the gif
from fractal_generator import FractalGenerator
from pygifsicle import optimize
import csv
import sys, getopt
from time import sleep
import sys
import math

# ignore the warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

try:
    opts, args = getopt.getopt(sys.argv[1:], "pfn:i:")
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

isPreview = False
force = False
numImagesToProcess = 0
specificImage = ""

for o, a in opts:
    if o == "-p":
        isPreview = True
    elif o == "-f":
        force = True
    elif o == "-n":
        numImagesToProcess = int(a)
    elif o == "-i":
        specificImage = int(a)
    else:
        assert False, "unhandled option"

# return the solours according to the timelapse
def get_prismatic_colours(pct):
    keyframes = [
        [0.5, 1, 1],    # red
        [0.5, 0.75, 1], # orange
        [0.5, 0.5, 1],  # yellow
        [1, 0.5, 1],    # green
        [1, 0.5, 0.5],  # blue
        [1, 1, 0.5],    # indigo
        [0.5, 1, 0.5],  # violet
        [0.5, 1, 1]     # red again
    ]
    lowerKeyframeIndex = math.floor(pct * (len(keyframes)-1))
    lowerKeyframe = keyframes[lowerKeyframeIndex]
    higherKeyframe = keyframes[lowerKeyframeIndex + 1]

    pctLowerKeyframe = lowerKeyframeIndex / len(keyframes)
    pctHigherKeyframe = (lowerKeyframeIndex + 1) / len(keyframes)

    interKeyframePct = min(1, (pct - pctLowerKeyframe) / (pctHigherKeyframe - pctLowerKeyframe))

    fgMultiplier = 1
    bgMultiplier = 6
    
    f1 = fgMultiplier * ((lowerKeyframe[0] * (1-interKeyframePct)) + (higherKeyframe[0] * (interKeyframePct)))
    f2 = fgMultiplier * ((lowerKeyframe[1] * (1-interKeyframePct)) + (higherKeyframe[1] * (interKeyframePct)))
    f3 = fgMultiplier * ((lowerKeyframe[2] * (1-interKeyframePct)) + (higherKeyframe[2] * (interKeyframePct)))
    b1 = 0.1#bgMultiplier * ((lowerKeyframe[0] * (1-interKeyframePct)) + (higherKeyframe[0] * (interKeyframePct)))
    b2 = 0.1#bgMultiplier * ((lowerKeyframe[1] * (1-interKeyframePct)) + (higherKeyframe[1] * (interKeyframePct)))
    b3 = 0.1#bgMultiplier * ((lowerKeyframe[2] * (1-interKeyframePct)) + (higherKeyframe[2] * (interKeyframePct)))

    return f1, f2, f3, b1, b2, b3


# define the number of frames to generate and the total time taken
def generate_julia_gif(filename, b1, b2, b3, f1, f2, f3, isPrismatic, a, b, r, frames, rotation, frameWidth, frameHeight, pixelWidth, pixelHeight, isPreview, isReversed):
    
    if isPreview:
        frames = 1
    #frames = 90
    framerate = 30
    total_time = frames / framerate

    images = []

    m = FractalGenerator()
    m.set_grid(start_x=-(frameWidth/2), end_x=(frameWidth/2),
        start_y=-(frameHeight/2), end_y=(frameHeight/2),
        resolution_x=pixelWidth, resolution_y=pixelHeight,
        threshold=2.9)

    for i in range(0, frames, 1):
        
        
        
        # Use the periodicity in c to generate a looping gif
        theta = 2 * i * np.pi / frames

        c = -(a - r * np.cos(theta)) - (b + r * np.sin(theta)) * 1j
        m.generate_julia(iterations=300, c=c)

        if isPrismatic:
            _f1, _f2, _f3, _b1, _b2, _b3 = get_prismatic_colours(i/frames)
        else:
            _f1 = f1
            _f2 = f2
            _f3 = f3
            _b1 = b1
            _b2 = b2
            _b3 = b3

        im = m.get_coloured_grid(_f1, _f2, _f3, _b1, _b2, _b3)

        # progress bar
        bar_len = 20
        pct_complete = round(100.0 * i / frames, 1)
        bar_str = '=' * round(bar_len / 100 * pct_complete)
        sys.stdout.write('\r')
        sys.stdout.write('Generating %s [%s] %s%s\r' % (filename, bar_str, pct_complete, '%'))
        sys.stdout.flush()
        
        im = im.rotate(rotation, expand=1)
        images.append(np.array(im))
        

    sys.stdout.write('%s completed' % (filename))

    if isReversed:
        images.reverse()

    # Write out our gif
    #filename = os.path.join(gif_dir, filename)
    imageio.mimsave(filename, images,'GIF', duration=total_time/frames)

    # optimize the gif
    optimize(filename)



#output_dir = "images"
gif_dir = "gifs"
preview_dir = "preview"
if not os.path.exists(preview_dir):
    os.makedirs(preview_dir)
if not os.path.exists(gif_dir):
    os.makedirs(gif_dir)
    

with open('csv/fractaloops - master.csv', newline='') as f:
    reader = csv.reader(f)
    headers = next(reader) 
    numImagesProcessed = 0
    for data in reader:
        
        # only process specific file
        if specificImage and str(specificImage) != str(data[0]):
            continue

        # only process n images
        if numImagesToProcess>0 and numImagesProcessed >= numImagesToProcess:
            exit()

        # if any cells are missing, skip
        if not all(data):
            continue

        # if file exists, skip
        if isPreview:
            filename = os.path.join(preview_dir, data[0] + ".gif")
        else:
            filename = os.path.join(gif_dir, data[0] + ".gif")

        if not force and os.path.exists(filename):
            continue
        
        if int(data[4])==10:
            isPrismatic = True
        else:
            isPrismatic = False
        
        if int(data[23]==1):
            isReversed = True
        else:
            isReversed = False

        # filename, b1, b2, b3, f1, f2, f3, a, b, r, frames, rotation, frameWidth, frameHeight, pixelWidth, pixelHeight, reversed
        generate_julia_gif(
            filename,
            float(data[8]),
            float(data[9]),
            float(data[10]),
            float(data[11]),
            float(data[12]),
            float(data[13]),
            isPrismatic,
            float(data[14]),
            float(data[15]),
            float(data[16]),
            int(data[17]),
            int(data[18]),
            float(data[19]),
            float(data[20]),
            int(data[21]),
            int(data[22]),
            isPreview,
            isReversed
        )
        
        numImagesProcessed += 1
    
    