import argparse
import numpy as np
from PIL import Image
from scipy import weave
import logging


def img2list(imgPath):
    """
    Reads an image.
    Returns image as a list
    """
    logging.info("Converting from image to list.")
    data = np.array(Image.open(imgPath), dtype=np.float)
    h, w = data.shape[:2]
    return data, h, w

def list2img(data,imgPath):
    """
    Writes data to outPath
    """
    logging.info("Converting from list to image.")
    data.astype(np.float)
    Image.fromarray(data).convert("RGB").save(imgPath)

def denoise(data,h,w, kappa=0.1, iter=10):
    """
    Runs a denoise algorithm on a given arary.
    Returns denoised channel.
    """
    logging.info("Running denoise.")
    data_new = data.copy()
    tmp = data.copy()
    in_vars = ["data","data_new","tmp","kappa", "iter", "h", "w"]
    code=r"""
        for (int round=0; round<iter; round++)
        {
            for (int i=1; i<h-1; i++)
            {
                for (int j=1; j<w-1; j++)
                {
                    data_new(i,j) = data(i,j) + kappa*(data(i-1,j)
                    +data(i,j-1) -4*data(i,j) +data(i,j+1)
                    +data(i+1,j));
                }
            }
            tmp = data;
            data = data_new;
            data_new = tmp;
        }
    """

    comp=weave.inline(code,
                      in_vars,
                      type_converters=weave.converters.blitz)
    return data


def run(source, target, shouldDenoise, kappa, iterations):
    """
    Runs the program
    """
    logging.info("Starting program.")
    imgList, h, w = img2list(source)
    if shouldDenoise:
        imgList = denoise(imgList, h, w, kappa, iterations)
    list2img(imgList, target)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--source", default="disasterbefore.jpg",
                        help="Path to source image")
    parser.add_argument("-o","--target", help="Path to resulting image",
                        default="disasterafter.weave.jpg")
    parser.add_argument("-k","--kappa", default=0.1,
                        help="Value between 0 and 1.", type=float)
    parser.add_argument("-i","--iter", default=10,
                        help="Times do do denoising", type=int)
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Be verbose about what's going on.")

    args = parser.parse_args()


    if args.verbose:
        logging.basicConfig(format='> %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='> %(message)s', level=logging.CRITICAL)


    run(args.source, args.target, True, args.kappa, args.iter)
