##Running the programs

Run from oblig03 folder

Python version
`python MyImgTool/denoise.py -s disasterbefore.jpg -t disasterafter.python.jpg`

Weave version
`python MyImgTool/denoise.weave.py -s disasterbefore.jpg -t disasterafter.weave.jpg`

### Note
The arguments specified here is the default ones so you don't actually need
to include them if you are not going to specify other paths.


## Creating diffs
The differences between generated disasterafter images can be hard to spot
but the `compare` command can aid.

Hat tip: ironhouzi

### Requirements
- Imagemagick  
On OSX you can install this with `brew install imagemagick`

### Creating the diffs
*The options works if you use the default paths when denoising images,
but it should be easy to alter.*

**Python**
`compare disasterafter.jpg disasterafter.python.jpg -compose src diff.python.png`

**Weave**
`compare disasterafter.jpg disasterafter.weave.jpg -compose src diff.weave.png`
