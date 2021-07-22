#!/bin/bash
# Usage: Batch convert NIFTI (*.nii) files to MINC (*.mnc) files
# $ ./NIFTI_to_MNC.sh

if ! command -v nii2mnc &> /dev/null
then
    echo "MINC Toolkit could not be found. Please install it and then run this again"
    exit
fi


for file in *nii; do
echo "Processing ${file}"
    nii2mnc "$file" "${file%.*}.mnc" |& tee ./"CT_log_details_${file%.*}.txt"
done
echo "All NIFTI files have been transformed to MINC files"

# For more information check: http://bic-mni.github.io/man-pages/man/nii2mnc.html