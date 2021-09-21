#!/bin/bash

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2).

# This is a script for creating Jacobian determinants. These volumes describe the amount of volume expansion (J > 1) or shrinkage (J < 1) at each voxel. As such, they can be used for voxel-wise analyses of shape or form, depending on how the determinants are derived. One might want to test for significant differences among experimental groups at each voxel, or perhaps compute the variance or amount of variance explained (R^2) at each voxel. A variety of statistical parametric mapping procedures can be performed. 

# Define a list of specimens and the atlas.
FILENAME="/path/to/MNC/<spec_list.txt>"
ATLAS="<.mnc>"

# Resolution of the atlas, assuming an isotropic scan.
ATLAS_RES=$(mincinfo ${ATLAS} -attvalue zspace:step)
# Blurring factor of 5 to blur the determinants.
BLUR_RES=$(awk "BEGIN {BLUR=$ATLAS_RES*5; print BLUR}")

# Start while loop.
while read -r line
do 
	# Input specimen image info.
	Biosample="${line}.mnc"
	# Concatenate affine and non-linear transformations to analyze differences in form (i.e. shape scaled up by the affine transform). To analyze shape, one can just use the non-linear transformation (*_ANTS_nl.xfm).  
	xfmconcat -clobber ${Biosample}_lsq12_2.xfm ${Biosample}_ANTS_nl.xfm ${Biosample}_form.xfm
	# Invert the transformations.
	xfminvert -clobber ${Biosample}_form.xfm ${Biosample}_form_inverted.xfm
	xfminvert -clobber ${Biosample}_ANTS_nl.xfm ${Biosample}_shape_inverted.xfm
	# Compute the displacements from every voxel in the reference ATLAS to every voxel in the target image. 
	minc_displacement -clobber ${ATLAS} ${Biosample}_form_inverted.xfm ${Biosample}_form_inverted_displacement.mnc
	minc_displacement -clobber ${ATLAS} ${Biosample}_shape_inverted.xfm ${Biosample}_form_inverted_displacement.mnc
	# Calculate the determinants.
	mincblob -clobber -determinant -clobber ${Biosample}_form_inverted_displacement.mnc ${Biosample}_form_inverted_determinant.mnc
	mincblob -clobber -determinant -clobber ${Biosample}_shape_inverted_displacement.mnc ${Biosample}_shape_inverted_determinant.mnc
	# Add 1 to determinant volumes, because it is subtracted in the det. calculation.
	mincmath -add -const 1 ${Biosample}_form_inverted_determinant.mnc ${Biosample}_form_inverted_determinant_p1.mnc
	mincmath -add -const 1 ${Biosample}_shape_inverted_determinant.mnc ${Biosample}_shape_inverted_determinant_p1.mnc
	# Generally, you want to blur the determinants because they can be quite noisy for images with millions of voxels. Consider blurring by a factor of 5-10. For example, if your RESolution is 35 microns, let's try BLURring with a 200 micron (0.2 mm) isotropic blurring kernel (-fwhm 0.2). 
	mincblur -clobber -fwhm ${BLUR_RES} ${Biosample}_form_inverted_determinant_p1.mnc ${Biosample}_form_inverted_determinant_p1
	mincblur -clobber -fwhm ${BLUR_RES} ${Biosample}_shape_inverted_determinant_p1.mnc ${Biosample}_shape_inverted_determinant_p1
done < "${FILENAME}"
