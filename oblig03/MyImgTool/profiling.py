from denoise import denoise as python_denoise
from denoise_weave import denoise as weave_denoise

if __name__=="__main__":


    # print cProfile.run("denoise(imgList,h,w,args.kappa,args.iter)", "numpy_timing")
    # pstats.Stats("numpy_timing").sort_stats("cumulative").print_stats()
