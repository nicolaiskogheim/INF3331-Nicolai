from PIL import Image
import cProfile
import pstats
import argparse
import logging


def img2list(imgPath):
    """
    Reads an image.
    Returns image as a list
    """
    logging.info("Converting from image to list.")
    im = Image.open(imgPath)
    data = list(im.getdata())
    w, h = im.size
    return data,h,w

def list2img(data,h,w,imgPath):
    """
    Writes data to outPath
    """
    logging.info("Converting from list to image.")
    im = Image.new("L", (w, h))
    im.putdata(data)
    im.save(imgPath)

def denoise(data,h,w, kappa=0.1, iter=10):
    """
    Runs a denoise algorithm on a given arary.
    Returns denoised channel.
    """
    logging.info("Running denoise.")
    for _ in xrange(0,iter):
        for i in xrange(1, w-1):
            for j in xrange(1, h-1):
                data[j*w+i] += \
                              kappa*(data[(j-1)*w+i]
                                   + data[j*w+(i-1)]
                                   - 4*data[j * w + i]
                                   + data[j*w+(i+1)]
                                   + data[i+ w * (j+1)]
                                   )
    return data

def run(source, target, shouldDenoise, kappa, iterations):
    """
    Runs the program
    """
    logging.info("Starting program.")
    imgList, h, w = img2list(source)
    if shouldDenoise:
        imgList = denoise(imgList, h, w, kappa, iterations)
    list2img(imgList, h, w, target)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--source", help="Path to source image",
                        default="disasterbefore.jpg")
    parser.add_argument("-o","--target", help="Path to resulting image",
                        default="disasterafter.python.jpg")
    parser.add_argument("-k","--kappa", default=0.1,
                        help="Value between 0 and 1.")
    parser.add_argument("-i","--iter", default=10,
                        help="Times do do denoising")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Be verbose about what's going on.")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(format='> %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='> %(message)s', level=logging.CRITICAL)

    run(args.source, args.target, True, args.kappa, args.iter)
