import cProfile
import pstats
from denoise import run  as python_denoise
from denoise_weave import run as weave_denoise
from denoise_colors import run as color_denoise

image_in_bnw="disasterbefore.jpg"
image_in_color="disastercolor.jpg"
image_out_python="disasterafter.python.profiling.jpg"
image_out_weave="disasterafter.weave.profiling.jpg"
image_out_color="disasterafter.color.profiling.jpg"

kappa=0.1
iter=10

if __name__=="__main__":
    cProfile.run("python_denoise(image_in_bnw,image_out_python,True,kappa,iter)", "python_timing")
    cProfile.run("weave_denoise(image_in_bnw,image_out_weave,True,kappa,iter)", "weave_timing")
    cProfile.run("color_denoise(image_in_color,image_out_color,True,kappa,iter,red=10,hue=10)", "color_timing")

    stats = pstats.Stats("python_timing")
    stats.add("weave_timing")
    stats.add("color_timing")

    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats(20)
