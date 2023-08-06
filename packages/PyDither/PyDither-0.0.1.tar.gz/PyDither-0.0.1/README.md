# image-dithering-python
python implementation for image dithering


## Quickstart
This library performs image dithering.

## Installation

To install, run:
```
$ pip install PyDither
```

## Usage:
```Python
	import cv2
	import Dither
	
	img = cv2.imread('images/img1.jpg', 0)						# read image

	out = Dither.dither(img, 'simple2D', resize=True)			# perform image dithering
	cv2.imshow('dithered image', out)							# display output
```
As easy as that!