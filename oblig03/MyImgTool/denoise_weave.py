import argparse
import numpy as np
from PIL import Image
from scipy import weave
import sys

def img2list(imgPath):
    data = np.array(Image.open(imgPath), dtype=np.float)
    h, w = data.shape[:2]
    return data, h, w

def list2img(data,h,w,imgPath):
    data.astype(np.float)
    Image.fromarray(data).convert("RGB").save(imgPath)

def denoise(data,h,w, kappa=0.1, iter=10):
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

def adjust_channel(*args, **kwargs):
    print "You cannot adjust channels on black and white images"
    sys.exit(0)

def run(source, target, shouldDenoise, kappa, iterations):
    imgList, h, w = img2list(source)
    if shouldDenoise:
        imgList = denoise(imgList, h, w, kappa, iterations)
    list2img(imgList, h, w, target)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--source", help="Path to source image",
                        default="disasterbefore.jpg")
    parser.add_argument("-t","--target", help="Path to resulting image",
                        default="disasterafter.weave.jpg")
    parser.add_argument("-k","--kappa", default=0.1,
            help="Value between 0 and 1.", type=float)
    parser.add_argument("-i","--iter", default=10,
            help="Times do do denoising", type=int)

    args = parser.parse_args();

    run(args.source, args.target, True, args.kappa, args.iter)
