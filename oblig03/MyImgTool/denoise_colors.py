import argparse
import numpy as np
from PIL import Image
from scipy import weave
import sys

def img2data(image_path):
    data = np.array(Image.open(image_path), dtype="uint8")

    if len(data.shape) == 2:
        print "The image you provided is black&white"
        print "Please use either denoise.py or denoise_weave.py for this."
        sys.exit(0)

    return data

def data2img(data, outPath):
    Image.fromarray(data.astype('uint8')).save(outPath)


def rgb2hsi(data):
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

def denoise(data, kappa=0.1, iter=10):
    h,w = data.shape[:2]
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



if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Utilities for color images")
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
    parser.add_argument("-r","--red", help="Adjust red channel with positive or negative int",
                        type=int,default=0)
    parser.add_argument("-g","--green", help="Adjust green channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-b","--blue", help="Adjust blue channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-u","--hue", help="Adjust hue channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-s","--saturation", help="Adjust saturation channel with positive or negative int",
                        type=float, default=0.)
    parser.add_argument("-i","--intensity", help="Adjust intensity channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-t","--timeit", help="Prints execution time", action="store_true")
    
    args = parser.parse_args()

    data = img2data(args.source)

