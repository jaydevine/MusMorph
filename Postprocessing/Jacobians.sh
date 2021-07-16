#!/bin/bash

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2).

# This is a script for creating Jacobian determinants. These volumes describe the amount of volume expansion (J > 1) or shrinkage (J < 1) at each voxel. As such, they can be used for voxel-wise analyses of shape or form, depending on how the determinants are derived. One might want to test for significant differences among experimental groups at each voxel, or perhaps compute the variance or amount of variance explained (R^2) at each voxel. A variety of statistical parametric mapping proceduRES can be performed. 

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
	SpecID="${line}.mnc"
	# Concatenate affine and non-linear transformations to analyze differences in form (i.e. shape scaled up by the affine transform). To analyze shape, one can just use the non-linear transformation (*_ANTS_nl.xfm).  
	xfmconcat -clobber ${SpecID}_lsq12_2.xfm ${SpecID}_ANTS_nl.xfm ${SpecID}_form.xfm
	# Invert the transformations.
	xfminvert -clobber ${SpecID}_form.xfm ${SpecID}_form_inverted.xfm
	xfminvert -clobber ${SpecID}_ANTS_nl.xfm ${SpecID}_shape_inverted.xfm
	# Compute the displacements from every voxel in the reference ATLAS to every voxel in the target image. 
	minc_displacement -clobber ${ATLAS} ${SpecID}_form_inverted.xfm ${SpecID}_form_inverted_displacement.mnc
	minc_displacement -clobber ${ATLAS} ${SpecID}_shape_inverted.xfm ${SpecID}_form_inverted_displacement.mnc
	# Calculate the determinants.
	mincblob -clobber -determinant -clobber ${SpecID}_form_inverted_displacement.mnc ${SpecID}_form_inverted_determinant.mnc
	mincblob -clobber -determinant -clobber ${SpecID}_shape_inverted_displacement.mnc ${SpecID}_shape_inverted_determinant.mnc
	# Add 1 to determinant volumes, because it is subtracted in the det. calculation.
	mincmath -add -const 1 ${SpecID}_form_inverted_determinant.mnc ${SpecID}_form_inverted_determinant_p1.mnc
	mincmath -add -const 1 ${SpecID}_shape_inverted_determinant.mnc ${SpecID}_shape_inverted_determinant_p1.mnc
	# Generally, you want to blur the determinants because they can be quite noisy for images with millions of voxels. Consider BLURring by a factor of 5-10. For example, if your RESolution is 35 microns, let's try BLURring with a 200 micron (0.2 mm) isotropic BLURring kernel (-fwhm 0.2). 
	mincblur -clobber -fwhm ${BLUR_RES} ${SpecID}_form_inverted_determinant_p1.mnc ${SpecID}_form_inverted_determinant_p1
	mincblur -clobber -fwhm ${BLUR_RES} ${SpecID}_shape_inverted_determinant_p1.mnc ${SpecID}_shape_inverted_determinant_p1
done < "${FILENAME}"
