import argparse
import numpy as np
from PIL import Image
from scipy import weave
import sys

def img2data(source):
    data = np.array(Image.open(source), dtype="uint8")

    if len(data.shape) == 2:
        print "The image you provided is black&white"
        print "Please use either denoise.py or denoise_weave.py for this."
        sys.exit(0)

    return data

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Utilities for color images")
    parser.add_argument("-f","--source", help="Path to source image",
                        default="disastercolors.jpg")
    parser.add_argument("-t","--target", help="Path to resulting image",
                        default="disastercolors.after.jpg")
    parser.add_argument("-d","--denoise", help="Denoise image (default false)",
                        action="store_true", default=False)
    parser.add_argument("-k", "--kappa", help="Parameter to denoise",
                        type=float, default=0.1)
    parser.add_argument("-n","--iterations", help="Parameter to denoise",
                        type=int, default=10)
    parser.add_argument("-r","--red", help="Adjust red channel with positive or negative int",
                        type=int,default=0)
    parser.add_argument("-b","--blue", help="Adjust blue channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-g","--green", help="Adjust green channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-u","--hue", help="Adjust hue channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-s","--saturation", help="Adjust saturation channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-i","--intensity", help="Adjust intensity channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-t","--timeit", help="Prints execution time", action="store_true")
    
    args = parser.parse_args()

    data = img2data(args.source)
    #data2img(data)
    # rgb to hsi
    #if denoise
        #denoise
    #alter hsi's
    #hsi 2 rbg
    #alter colors
    # nup2img

