#!/bin/bash

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2).

# This is an isotropic downsampling and intensity correction script. It has a function that will read in the input image resolution, find the scaling factor that relates the this resolution to the (presumably lower) atlas resolution, read in the z,y,x voxel lengths, then reduce them to what they should be at the new res. This downsampled image is then corrected for intensity inhomogeneities, and the image values are normalized between 0 and 1. 

# Specimen list
filename="/path/to/MNC/<spec_list.txt>"

# Start while loop.
while read -r line
do 
	# Input and output name info.
	atlas="<.mnc>" # Enter atlas name.
	orig_name="${line}.mnc"
	ds_name="${line}_ds.mnc"
	corr_name="${line}_ds_corr.mnc"
	norm_name="${line}_ds_norm.mnc"
	# Image dimension info.
	Z=$(mincinfo -dimlength zspace ${orig_name})
	Y=$(mincinfo -dimlength yspace ${orig_name})
	X=$(mincinfo -dimlength xspace ${orig_name})
	# Image res info, assuming isotropic res. 
	ATLAS_RES=$(mincinfo ${atlas} -attvalue zspace:step)
	IMAGE_RES=$(mincinfo ${orig_name} -attvalue zspace:step)
	SCALAR=$(awk "BEGIN {scale=$ATLAS_RES/$IMAGE_RES; print scale}")
	# Now divide Z,Y,X by SCALAR.
	Z_DS=$(awk "BEGIN {z=$Z/$SCALAR; print int(z+0.5)}")
	Y_DS=$(awk "BEGIN {y=$Y/$SCALAR; print int(y+0.5)}")
	X_DS=$(awk "BEGIN {x=$X/$SCALAR; print int(x+0.5)}")
	# Run resampling. We've assumed the image origin is 0,0,0.
	mincresample -clobber -zstart 0 -ystart 0 -xstart 0 -zstep ${ATLAS_RES} -ystep ${ATLAS_RES} -xstep ${ATLAS_RES} -znelements ${Z_DS} -ynelements ${Y_DS} -xnelements ${X_DS} ${orig_name} ${ds_name}
	# Run intensity correction.
	nu_correct ${ds_name} ${corr_name}
	# Run intensity normalization between 0 and 1. 
	mincnorm -out_floor 0 -out_ceil 1 ${corr_name} ${norm_name}
done < "${filename}"
