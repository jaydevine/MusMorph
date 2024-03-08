#!/bin/bash

# This script will convert Scanco .aim/.txt files to .mnc.

# Check for MINC Toolkit
if ! command -v rawtominc &> /dev/null; then
    echo "MINC Toolkit could not be found. Please install it and then run this again."
    exit 1
fi

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# You only need to uncomment and edit the variables below if you don't use raw input.

# Path to specimen list .txt file.
# FILENAME="/path/to/<PROJECT>/Source/<>.txt"

# Path to original images.
# SOURCE_PATH="/path/to/<PROJECT>/Source/Orig/"

# Path to specimen list .txt file.
read -p "Enter the path to the file containing the list of specimen names (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/spec_list.txt): " FILENAME

# Path to original images.
read -p "Enter the path to the directory containing the original images (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/Orig/): " SOURCE_PATH

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Read file containing list of specimen names
while IFS= read -r Biosample || [[ -n "$Biosample" ]]; do
    echo "Working on $Biosample at $SOURCE_PATH"
    # Define file paths
    TXTFILE="${SOURCE_PATH}${Biosample}.txt"
    AIMFILE="${SOURCE_PATH}${Biosample}.aim"
    MNCFILE="${SOURCE_PATH}${Biosample}.mnc"

    # Convert DOS to Unix format
    dos2unix "$TXTFILE"

    # Extract necessary information
    OFFSET_LINE=$(grep offset "$TXTFILE")
    ARR_OFF=($OFFSET_LINE)
    ACT_OFFSET=${ARR_OFF[6]:0:4}

    DIMENSIONS=$(grep -m 1 dim "$TXTFILE")
    ARR_DIM=($DIMENSIONS)
    ACT_X=${ARR_DIM[1]}
    ACT_Y=${ARR_DIM[2]}
    ACT_Z=${ARR_DIM[3]}

    RESOLUTION=$(grep element "$TXTFILE")
    ARR_RES=($RESOLUTION)
    RES_X=${ARR_RES[4]}
    RES_Y=${ARR_RES[5]}
    RES_Z=${ARR_RES[6]}

    # Convert raw data to .mnc file
    rawtominc -input "$AIMFILE" -short -scan_range -clobber -skip "$ACT_OFFSET" -xstep "$RES_X" -ystep "$RES_Y" -zstep "$RES_Z" -origin 0 0 0 "$MNCFILE" "$ACT_Z" "$ACT_Y" "$ACT_X"

    # Create montage image
    QCPOST="_QC.png"
    QCFILE="${SOURCE_PATH}${Biosample}${QCPOST}"
    LABPOST="_QC_labeled.png"
    LABFILE="${SOURCE_PATH}${Biosample}${LABPOST}"
    mincpik -clobber -scale 20 -triplanar "$MNCFILE" "$QCFILE"
    convert -label "$Biosample" "$QCFILE" "$LABFILE"

    # Build full montage command
    MONTAGE_CMD+=" $LABFILE"
done < "$FILENAME"

# Create a montage of the converted images
MONTAGE_CMD="montage -geometry +2+2 $MONTAGE_CMD ${SOURCE_PATH}Montage.png"
eval "$MONTAGE_CMD"
