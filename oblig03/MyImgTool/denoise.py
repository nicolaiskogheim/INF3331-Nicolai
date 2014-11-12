from PIL import Image
import cProfile
import pstats
import argparse

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

    args = parser.parse_args();

    imgList, h, w = img2list(args.source)
    
    data = denoise(imgList,h,w, args.kappa, args.iter)

    list2img(data,h,w,args.target)
