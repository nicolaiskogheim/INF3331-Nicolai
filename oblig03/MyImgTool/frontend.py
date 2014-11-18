import argparse
from textwrap import dedent
import logging
import cProfile
import pstats
import denoise as python_denoise
import denoise_weave as weave_denoise
import denoise_colors as color_denoise


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Utilities for images")
    # path params
    parser.add_argument("-f","--source", help="Path to source image",
                        default="disastercolor.jpg")
    parser.add_argument("-o","--target", help="Path to resulting image",
                        default="disaster.after.frontend.jpg")
    # denoise params
    parser.add_argument("-d","--denoise",
                        # dest='backend',
                        const="color",
                        default=False,
                        action="store",
                        nargs="?",
                        type=str,
                        choices=["color","python","weave"],
                        help=dedent("""\
                            Denoise image (default false).
                            When argument is present, defaults
                            to color/weave backend.
                            Specify `-d python` or
                            `-d weave` for b&w images.
                            """)
                        )
    parser.add_argument("-k", "--kappa", help="Parameter to denoise",
                        type=float, default=0.1)
    parser.add_argument("-n","--iterations", help="Parameter to denoise",
                        type=int, default=10)
    # rgb params
    parser.add_argument("-r","--red", help="Adjust red channel with positive or negative int",
                        type=int,default=0)
    parser.add_argument("-g","--green", help="Adjust green channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-b","--blue", help="Adjust blue channel with positive or negative int",
                        type=int, default=0)
    # hsi params
    parser.add_argument("-u","--hue", help="Adjust hue channel with positive or negative int",
                        type=int, default=0)
    parser.add_argument("-s","--saturation", help="Adjust saturation channel with positive or negative int",
                        type=float, default=0.)
    parser.add_argument("-i","--intensity", help="Adjust intensity channel with positive or negative int",
                        type=int, default=0)


    parser.add_argument("-t","--timeit", help="Prints execution time", action="store_true")
    parser.add_argument("-v", "--verbose", help="Be verbose about what's happening", action="store_true")

    args = parser.parse_args()


    if args.verbose:
        logging.basicConfig(format='> %(message)s', level=logging.INFO)
    else:
        logging.basicConfig(format='> %(message)s', level=logging.CRITICAL)

    if args.denoise:
        shouldDenoise = True
    else:
        shouldDenoise = False

    color = False
    if args.denoise == "python":
        logging.info("Using pure python backend for black and white image.")
        backend = python_denoise
    elif args.denoise == "weave":
        logging.info("Using numpy/weave backend for black and white image.")
        backend = weave_denoise
    else:
        logging.info("Using numpy/weave backed for colored image.")
        backend = color_denoise
        color = True

    if color is False:
        source = "disasterbefore.jpg" if args.source is "disastercolor.jpg" else args.source
        logging.info("Starting program with image %s", source)

        if args.timeit:
            timing_name = "blacknwhite_timing"
            cProfile.run("backend.run(source, args.target, shouldDenoise,\
                          args.kappa, args.iterations)", timing_name)
        else:
            backend.run(source, args.target,
                        shouldDenoise, args.kappa, args.iterations)
    else:
        logging.info("Starting program with image %s", args.source)
        if args.timeit:
            timing_name = "color_timing"
            cProfile.run("backend.run(args.source, args.target,\
                                      shouldDenoise, args.kappa, args.iterations,\
                                      args.hue, args.saturation, args.intensity,\
                                      args.red, args.green, args.blue)", timing_name)
        else:
            backend.run(args.source, args.target,
                        shouldDenoise, args.kappa, args.iterations,
                        args.hue, args.saturation, args.intensity,
                        args.red, args.green, args.blue)
    if args.timeit:
        pstats.Stats(timing_name).strip_dirs().sort_stats("cumulative").print_stats(12)
