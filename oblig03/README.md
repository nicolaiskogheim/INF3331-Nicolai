##Running the programs

Run from oblig03 folder

Python version  
`python MyImgTool/denoise.py -f disasterbefore.jpg -o disasterafter.python.jpg`

Weave version  
`python MyImgTool/denoise_weave.py -f disasterbefore.jpg -o disasterafter.weave.jpg`

Color version  
`python MyImgTool/denoise_color.py -f disastercolor.jpg -o disasterafter.color.jpg -d`

Full blown from frontend  
`python MyImgTool/frontend.py -f disastercolor.jpg -o disasterafter.frontend.jpg -d -r 30 -s -.05`

### Note

The image path arguments specified here is the default ones so you  
don't actually need to include them if you are not going to specify other paths.

Creating diffs
--------------

The differences between generated disasterafter images can be hard to spot  
but the `compare` command can aid.

Hat tip: ironhouzi

### Requirements

-	Imagemagick  
	On OSX you can install this with `brew install imagemagick`

### Creating the diffs

*These options works if you use the default paths when denoising images,  
but it should be easy to alter.*

**Python**  
`compare disasterafter.jpg disasterafter.python.jpg -compose src diff.python.png`

**Weave**  
`compare disasterafter.jpg disasterafter.weave.jpg -compose src diff.weave.png`

*There wasn't a color example result provided with the assignment,  
but you can of course diff two color images on your own by altering the examples above.*
