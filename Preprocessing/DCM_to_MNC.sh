#!/bin/bash

# This script batch converts DICOM (.dcm) files to MINC (.mnc) files. Each individual should have a separate directory containing a stack of DICOM slices. Note that this command has many options and is somewhat error prone. For more information, please visit http://bic-mni.github.io/man-pages/man/dcm2mnc.html.

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v dcm2mnc &> /dev/null; then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit 1
fi

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# You only need to uncomment and edit the variables below if you don't use raw input.

# Path to original images.
# SOURCE_PATH="/path/to/<PROJECT>/Source/Orig/"

# Path to original images.
read -p "Enter the path to the directory containing the original DICOM stacks (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/Orig/): " SOURCE_PATH

cd ${SOURCE_PATH}
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Run dcm2mnc command. This command will convert each directory into a .mnc file. Each .mnc file will be named according to the directory. 
dcm2mnc -usecoordinates -dname '' -fname '%N' ./* .
