#!/bin/bash

# This script batch converts DICOM (.dcm) files to MINC (.mnc) files. Each individual should have a separate DICOM directory. Note that this command has many options and is somewhat error prone. For more information, please visit http://bic-mni.github.io/man-pages/man/dcm2mnc.html or 

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2). Check:
if ! command -v dcm2mnc &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit
fi

# Run dcm2mnc command. This command will convert each directory into a .mnc file. Each .mnc file will be named according to the directory. 
dcm2mnc -usecoordinates -dname '' -fname '%N' ./* .
