import os
from PIL import Image
import sys, getopt
import csv

# ignore warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

try:
    opts, args = getopt.getopt(sys.argv[1:], "pfn:i:")
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

specificImage = ""

for o, a in opts:
    if o == "-i":
        specificImage = int(a)
    else:
        assert False, "unhandled option"



def analyseImage(path):
    '''
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode 
    before processing all frames.
    '''
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


def processImage(file_in, file_out, frame):
    '''
    Iterate the GIF, extracting each frame.
    '''
    mode = analyseImage(file_in)['mode']
    
    im = Image.open(file_in)

    i = 0
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    
    try:
        while True:
            #print(saving %s (%s) frame %d, %s %s" % (file_in, mode, i, im.size, im.tile))
            
            '''
            If the GIF uses local colour tables, each frame will have its own palette.
            If not, we need to apply the global palette to the new frame.
            '''
            if not im.getpalette():
                im.putpalette(p)
            
            new_frame = Image.new('RGBA', im.size)
            
            '''
            Is this file a "partial"-mode GIF where frames update a region of a different size to the entire image?
            If so, we need to construct the new frame by pasting it on top of the preceding frames.
            '''
            if mode == 'partial':
                new_frame.paste(last_frame)
            
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            
            if i==frame:
                new_frame.save('%s.png' % (os.path.join(file_out)), 'PNG')
                im.close()
                break
            

            i += 1

            
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass


#output_dir = "images"
thumb_dir = "../app/public/thumbs"
if not os.path.exists(thumb_dir):
    os.makedirs(thumb_dir)
    

with open('csv/fractaloops - master.csv', newline='') as f:
    reader = csv.reader(f)
    headers = next(reader) 
    numImagesProcessed = 0
    for data in reader:
        
        filename = os.path.join("gifs/", data[0] + ".gif")

        # only process specific file
        if specificImage and str(specificImage) != str(data[0]):
            continue

        if not os.path.exists(filename):
            continue

        processImage(
            filename,
            os.path.join(thumb_dir, data[0]),
            1
        )
    
    