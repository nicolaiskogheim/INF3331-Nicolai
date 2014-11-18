from PIL import Image
import cProfile
import pstats
import argparse
import sys

def img2list(imgPath):
    im = Image.open(imgPath)
    data = list(im.getdata())
    w, h = im.size
    return data,h,w

def list2img(data,h,w,imgPath):
    im = Image.new("L", (w, h))
    im.putdata(data)
    im.save(imgPath)

def denoise(data,h,w, kappa=0.1, iter=10):
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

def adjust_channel(*args, **kwargs):
    print "You cannot adjust channels on black and white images"
    sys.exit(0)

def run(source, target, kappa, iter):
    imgList, h, w = img2list(source)
    data = denoise(imgList,h,w,kappa,iter)
    list2img(data,h,w,target)

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s","--source", help="Path to source image",
                        default="disasterbefore.jpg")
    parser.add_argument("-t","--target", help="Path to resulting image",
                        default="disasterafter.python.jpg")
    parser.add_argument("-k","--kappa", default=0.1,
                        help="Value between 0 and 1.")
    parser.add_argument("-i","--iter", default=10,
                        help="Times do do denoising")

    args = parser.parse_args()

    run(args.source, args.target)
