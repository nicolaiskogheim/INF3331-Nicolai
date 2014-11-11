import argparse
import numpy as np
from PIL import Image
from scipy import weave

def img2list(imgPath):
    data = np.array(Image.open(imgPath))
    h, w = data.shape[:2]
    return data, h, w

def list2img(data,h,w,imgPath):
    Image.fromarray(data).save(imgPath)

def denoise(data,h,w, kappa=0.1, iter=10):
    data_new = data.copy()
    in_vars = ["data","data_new","kappa", "iter", "h", "w"]
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
        }
        data = data_new;
    """
   
    comp=weave.inline(code,
                      in_vars,
                      type_converters=weave.converters.blitz) 
    return data

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("imgPathIn", help="Path to source image")
    parser.add_argument("imgPathOut", help="Path to resulting image")
    parser.add_argument("-k","--kappa", default=0.1,
            help="Value between 0 and 1.")
    parser.add_argument("-i","--iter", default=10,
            help="Times do do denoising")

    args = parser.parse_args();
    
    imgList, h, w = img2list(args.imgPathIn)

    data = denoise(imgList,h,w, args.kappa, args.iter)

    list2img(data,h,w,args.imgPathOut)