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
from PIL import Image, ImageFont, ImageDraw

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



# define the number of frames to generate and the total time taken
def generate_number_gif(filename, number):
    
    
    print("stamping gif ", number)

    gif = Image.open("gifs/" + number + ".gif").convert("RGBA")
    stamp = Image.new("RGBA", (350, 350), (255, 255, 255, 0))
    font = ImageFont.truetype("fonts/ostrich-regular.ttf", 26)

    draw = ImageDraw.Draw(stamp)

    draw.text((300,300), number, (0, 0, 0, 15), font=font)
    

    combined = Image.alpha_composite(gif, stamp)

    combined.save("stamped_gifs/" + number + ".gif")

    # rarity rating


    # save
    #stamp.save(filename, 'GIF', transparency=0)

    # optimize
    #optimize(filename)

    



#output_dir = "images"
gif_dir = "stamped_gifs"
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

        filename = os.path.join(gif_dir, data[0] + ".gif")

        # filename, number, x, y
        generate_number_gif(
            filename,
            data[0]
        )
        
        numImagesProcessed += 1


    
    