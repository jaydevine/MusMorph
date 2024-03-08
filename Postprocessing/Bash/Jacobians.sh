#!/bin/bash

# This is a script for creating Jacobian determinants. These volumes describe the amount of volume expansion (J > 1) or shrinkage (J < 1) at each voxel. As such, they can be used for voxel-wise analyses of shape or form, depending on how the determinants are derived. One might want to test for significant differences among experimental groups at each voxel, or perhaps compute the variance or amount of variance explained (R^2) at each voxel. A variety of statistical parametric mapping procedures can be performed. 

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2),
if ! command -v mincresample &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

# and minc-stuffs (https://github.com/Mouse-Imaging-Centre/minc-stuffs),
if ! command -v minc_displacement &> /dev/null
then
    echo "minc-stuffs could not be found. Please install it and then run this again."
    exit
fi

# Prompt for FILENAME
read -p "Enter the path to the file containing the list of specimen names (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/spec_list.txt): " FILENAME

# Prompt for ATLAS
read -p "Enter the full path to the atlas file (include .mnc extension; e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/MNC/Calgary_Adult_Skull_Atlas.mnc): " ATLAS

# Prompt for XFM_PATH
read -p "Enter the path to the XFM files (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/nl/Ana_Test/): " XFM_PATH

# Prompt for form determinants computation
read -p "Compute determinants for form? [true/false]: " compute_form
compute_form=${compute_form:-true}

# Prompt for shape determinants computation
read -p "Compute determinants for shape? [true/false]: " compute_shape
compute_shape=${compute_shape:-true}

# Prompt for blur factor
read -p "Enter the determinant blur factor, resulting in a resolution of atlas resolution * blur factor (default is 5): " blur_factor
blur_factor=${blur_factor:-5}

# While loop.
while read -r line
do 
    # Input specimen image info.
    Biosample="${line}"
    # Alter path to images.
    cd "${XFM_PATH}"
    echo "Working on ${Biosample} at ${XFM_PATH}."
    # Define resolution of the atlas, assuming an isotropic scan.
    ATLAS_RES=$(mincinfo ${ATLAS} -attvalue zspace:step)
    # Blurring factor of 5 to inevitably blur the determinants.
    BLUR_RES=$(awk -v blur=$blur_factor "BEGIN {print $ATLAS_RES * blur}")
    # Calculate the determinants.
    if [ "$compute_form" == "true" ]; then
        xfmconcat -clobber ${Biosample}_lsq12_2.xfm ${Biosample}_ANTS_nl.xfm ${Biosample}_form.xfm
        xfminvert -clobber ${Biosample}_form.xfm ${Biosample}_form_inverted.xfm
        minc_displacement -clobber ${ATLAS} ${Biosample}_form_inverted.xfm ${Biosample}_form_inverted_displacement.mnc
        mincblob -clobber -determinant -clobber ${Biosample}_form_inverted_displacement.mnc ${Biosample}_form_inverted_determinant.mnc
        mincmath -add -const 1 ${Biosample}_form_inverted_determinant.mnc ${Biosample}_form_inverted_determinant_p1.mnc
        mincblur -clobber -fwhm ${BLUR_RES} ${Biosample}_form_inverted_determinant_p1.mnc ${Biosample}_form_inverted_determinant_p1
    fi
    if [ "$compute_shape" == "true" ]; then
        xfminvert -clobber ${Biosample}_ANTS_nl.xfm ${Biosample}_shape_inverted.xfm
        minc_displacement -clobber ${ATLAS} ${Biosample}_shape_inverted.xfm ${Biosample}_shape_inverted_displacement.mnc
        mincblob -clobber -determinant -clobber ${Biosample}_shape_inverted_displacement.mnc ${Biosample}_shape_inverted_determinant.mnc
        mincmath -add -const 1 ${Biosample}_shape_inverted_determinant.mnc ${Biosample}_shape_inverted_determinant_p1.mnc
        mincblur -clobber -fwhm ${BLUR_RES} ${Biosample}_shape_inverted_determinant_p1.mnc ${Biosample}_shape_inverted_determinant_p1
    fi
done < "${FILENAME}"

echo "All outputs have been sent to ${XFM_PATH}."
