import argparse
import numpy as np
from PIL import Image
from scipy import weave
import sys
import logging

def img2list(image_path):
    """
    Reads an image.
    Returns image as a list
    """
    logging.info("Loading image %s", image_path)
    data = np.array(Image.open(image_path), dtype="uint8")

    if len(data.shape) == 2:
        print "The image you provided is black&white"
        print "Please use either denoise.py or denoise_weave.py for this."
        sys.exit(0)
    return data

def data2img(data, outPath):
    """
    Writes data to outPath
    """
    logging.info("Writing image to %s", outPath)
    Image.fromarray(data.astype('uint8')).save(outPath)


def rgb2hsi(data):
    """
    Converts array from rgb color space to hsi color space
    Returns data in hsi format.
    """
    logging.info("Converting from rgb to hsi.")
    i = np.mean(data, axis=2)

    s = np.copy(i)
    m = i == 0
    s[m] = 0
    rgbMin = np.amin(data, axis=2)
    s[~m] = 1 - rgbMin[~m]/i[~m]

    #TODO This is slow. Refactor so numpy can optimize this
    def hfunk(r,g,b):
        r, g, b = float(r), float(g), float(b)
        if r == g == b:
            return 0
        numerator= r - g/2 - b/2
        denominator=np.sqrt(r**2 + g**2 + b**2 - r*g - r*b - g*b)
        result = np.degrees(np.arccos(numerator/denominator))
        if g >= b:
            return result
        else:
            return 360 - result
    hfunk = np.vectorize(hfunk)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    h = hfunk(r,g,b)

    hsi = np.dstack((h,s,i))
    return hsi

def hsi2rgb(data):
    """
    Converts array from hsi color space to rgb color space.
    Returns data in rgb format.
    """
    logging.info("Converting from hsi to rgb.")
    h,s,i = data[:,:,0], data[:,:,1], data[:,:,2]
    r,g,b = np.copy(h),np.copy(s),np.copy(i)

    """
    In case the reader is not familar with numpy masks,
    here is an explanation.
    For every element in `r` and `h` (in the code below)
    if the `h` element equals 0, evaluate the expression
    on the right of the equals sign.
    So in this first code block, every element of `r`
    where the same index in `h` equals 0, the element
    in `r` will get new values.
    The other arrays (`g`,`b`,`i` and `s`) work the same
    since the mask is applied.
    The arrays need to have the same size and shape for
    this to work.
    """
    mask = h == 0
    r[mask], g[mask], b[mask] = \
            i[mask] + 2*i[mask]*s[mask], \
            i[mask] - i[mask]*s[mask], \
            i[mask] - i[mask]*s[mask], \

    m = (0 < h) & (h < 120)
    r[m], g[m], b[m] = \
            i[m]+i[m]*s[m]*(np.cos(np.radians(h[m]))/np.cos(np.radians(60 - h[m]))),\
            i[m]+i[m]*s[m]*(1-(np.cos(np.radians(h[m]))/np.cos(np.radians(60 - h[m])))),\
            i[m]-i[m]*s[m]

    m = h == 120
    r[m], g[m], b[m] = \
            i[m] - i[m]*s[m],\
            i[m] + 2*i[m]*s[m],\
            i[m] - i[m]*s[m]

    m = (120 < h) & (h < 240)
    r[m], g[m], b[m] = \
            i[m] - i[m]*s[m],\
            i[m]+i[m]*s[m]*(np.cos(np.radians(h[m] - 120))/np.cos(np.radians(180 - h[m]))),\
            i[m] + i[m]*s[m]*(1 - (np.cos(np.radians(h[m] - 120))/np.cos(np.radians(180 - h[m]))))

    m = h == 240
    r[m], g[m], b[m] = \
            i[m] - i[m] * s[m],\
            i[m] - i[m] * s[m],\
            i[m] + 2*i[m]*s[m]

    m = (240 < h) & (h <= 360)
    r[m], g[m], b[m] = \
            i[m] + i[m]*s[m]*(1 - np.cos(np.radians(h[m] - 240))/np.cos(np.radians(300 - h[m]))),\
            i[m] - i[m]*s[m],\
            i[m] + i[m]*s[m]*(np.cos(np.radians(h[m] - 240))/np.cos(np.radians(300 - h[m])))

    return np.dstack((r,g,b))

def denoise(channel, kappa=0.1, iter=10):
    """
    Runs a denoise algorithm on a given arary.
    Returns denoised channel.
    """
    logging.info("Running denoise.")
    h,w = channel.shape[:2]
    channel_new = channel.copy()
    tmp = channel.copy()
    in_vars = ["channel","channel_new","tmp","kappa", "iter", "h", "w"]
    code=r"""
        for (int round=0; round<iter; round++)
        {
            for (int i=1; i<h-1; i++)
            {
                for (int j=1; j<w-1; j++)
                {
                    channel_new(i,j) = channel(i,j) + kappa*(channel(i-1,j)
                    +channel(i,j-1) -4*channel(i,j) +channel(i,j+1)
                    +channel(i+1,j));
                }
            }
            tmp = channel;
            channel = channel_new;
            channel_new = tmp;
        }
    """

    comp=weave.inline(code,
                      in_vars,
                      type_converters=weave.converters.blitz)
    return channel

def adjust_channel(channel, channel_name, addend, max_value):
    """
    Takes an arbitrary numpy array and adds addend to every element.
    Addend can be a negative value.
    Returns adjusted array.
    """
    addend = float(addend)
    if addend == 0:
        return channel

    if np.absolute(addend) > max_value:
        err_msg = "The {0} channel can be adjusted up or down by maximum {1}"
        print err_msg.format(channel_name,max_value)
        print "Your value was %d" % addend
        sys.exit(0)

    logging.info("Adjusting the %s channel by %d.", channel_name, addend)
    channel = channel + addend
    channel[channel > max_value] = max_value
    channel[channel < 0] = 0

    return channel

def run(source, target, shouldDenoise, kappa, iterations, hue, saturation, intensity, red, green, blue):
    """
    Runs the program
    """
    logging.info("Starting program.")
    data = img2list(source)
    hsi = rgb2hsi(data)


    h,s,i = hsi[:,:,0], hsi[:,:,1], hsi[:,:,2]

    if shouldDenoise:
        denoise(i, kappa, iterations)
        denoise(s, kappa, iterations)

    h = adjust_channel(h, "hue", hue, 360)
    s = adjust_channel(s, "saturation", saturation, 1)
    i = adjust_channel(i, "intensity", intensity, 255)
    hsi = np.dstack((h,s,i))

    rgb = hsi2rgb(hsi)
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    r = adjust_channel(r, "red", red, 255)
    g = adjust_channel(g, "green", green, 255)
    b = adjust_channel(b, "blue", blue, 255)

    rgb = np.dstack((r,g,b))

    data2img(rgb,target)


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Utilities for color images")
    # denoise params
    parser.add_argument("-f","--source", help="Path to source image",
                        default="disastercolor.jpg")
    parser.add_argument("-o","--target", help="Path to resulting image",
                        default="disastercolor.after.jpg")
    parser.add_argument("-d","--denoise", help="Denoise image (default false)",
                        action="store_true", default=False)
    parser.add_argument("-k", "--kappa", help="Parameter to denoise",
                        type=float, default=0.1)
    parser.add_argument("-n","--iterations", help="Parameter to denoise",
                        type=int, default=10)
    # rgb params
    parser.add_argument("-r","--red", help="Adjust red channel with positive or negative int",
                        type=int,default=0)
    parser.add_argument("-g","--green", help="Adjust green channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-b","--blue", help="Adjust blue channel with positive or negative int",
                        type=int, default=0)
    # hsi params
    parser.add_argument("-u","--hue", help="Adjust hue channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-s","--saturation", help="Adjust saturation channel with positive or negative int",
                        type=float, default=0.)
    parser.add_argument("-i","--intensity", help="Adjust intensity channel with positive or negative int",
                        type=int, default=0)

    parser.add_argument("-t","--timeit", help="Prints execution time", action="store_true")
    parser.add_argument("-v", "--verbose", help="Be verbose about what's going on.", action="store_true")

    args = parser.parse_args()


    if args.verbose:
        logging.basicConfig(format='> %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='> %(message)s', level=logging.CRITICAL)

    run(args.source, args.target,
        args.denoise, args.kappa, args.iterations,
        args.hue, args.saturation, args.intensity,
        args.red, args.green, args.blue)
