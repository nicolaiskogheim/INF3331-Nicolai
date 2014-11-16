import cProfile
import pstats
from denoise import run  as python_denoise
from denoise_weave import run as weave_denoise

image_in_path="disasterbefore.jpg"
image_out_python="disasterafter.python.jpg"
image_out_weave="disasterafter.weave.jpg"

kappa=0.1
iter=10

if __name__=="__main__":
    cProfile.run("python_denoise(image_in_path,image_out_python,kappa,iter)", "python_timing")
    cProfile.run("weave_denoise(image_in_path,image_out_weave,kappa,iter)", "weave_timing")

    stats = pstats.Stats("python_timing")
    stats.add("weave_timing")

    stats.strip_dirs()
    stats.sort_stats("cumulative")
    stats.print_stats()
