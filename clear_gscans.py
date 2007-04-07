#!/usr/bin/env python
# $Date: 2007-04-07 14:27:44 $, $Revision: 1.4 $

from gimpfu import *

def clear(data, width, height):
	gimp.progress_init("Cleaning...")

	changed = False
	
	thres = 255**7 * 64
	for y in xrange(1, height-1):
		gimp.progress_update( ((y-2))/float(height-2) )

		row_a = data[y-1]
		row_b = data[y]
		row_c = data[y+1]
		for x in xrange(1, width-1):
			if row_b[x] == 255:
				continue

			a = row_a[x-1]
			b = row_a[x]
			c = row_a[x+1]

			d = row_b[x-1]
			f = row_b[x+1]

			g = row_c[x-1]
			h = row_c[x]
			i = row_c[x+1]

			if a*b*c*d*f*g*h*i >= thres:
				row_b[x] = 255
				changed  = True
	return changed


def python_clear_gscans(img, drawable, colnum=16, repeat=False):

	if img.base_type != 1: # not grayscale
		pdb.gimp_image_convert_grayscale(img)

	pdb.gimp_image_convert_indexed(
		img,
		0,	# no dither
		0,	# make palette
		colnum,	# colors num
		0,
		0,
		"",
	)
	
	pdb.gimp_image_convert_grayscale(img)

	
	drawable = img.active_layer
	width    = drawable.width
	height   = drawable.height
	pr = drawable.get_pixel_rgn(0, 0, width, height)
	
	gimp.progress_init("Loading image...")
	row  = [255]*(width+2)
	data = []
	data.append(row)
	for y in xrange(height):
		gimp.progress_update( y/float(height-1) )
		data.append( [255] + map(ord, pr[0:width,y]) + [255] )
	data.append(row)

	while clear(data, width+2, height+2) and repeat:
		pass
	
	gimp.progress_init("Saving back image...")
	for y in xrange(height):
		gimp.progress_update( y/float(height-1) )
		pr[0:width,y] = ''.join(map(chr, data[y+1][1:-1]))
	
	drawable.flush()
	

register(
        "python_fu_clear_gscans",
        "Clear grayscale scans",
        "Clear grayscale scans",
        "Wojciech Mula",
        "Wojciech Mula",
        "2007",
        "<Image>/Filters/_Clear gscans...",
        "RGB*, GRAY*",
        [
		(PF_INT, "colnum", "Color number", 16),
		(PF_BOOL, "repeat", "Repeat cleaning", False),
	],
        [],
        python_clear_gscans)

main()


