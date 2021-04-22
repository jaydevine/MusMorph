#!/bin/bash

# Dependencies required: MINC Toolkit (https://bic-mni.github.io/ or https://github.com/BIC-MNI/minc-toolkit-v2) and the dos2unix Bash package.

# Create a variable called filename that calls upon a .txt file of specimen names. 
filename="/path/to/<spec_list.txt>" 
# Invoke the montage command to produce an output .png containing images of the newly created .mnc files. 
montage_cmd="montage -geometry +2+2"
# Start a while loop to read your filename line by line. 
while read -r line
do
	# The 'name' variable becomes each line within filename. 
	name="$line"
	cd "/path/to/aim"
	echo "Working on $name at /path/to/aim"
	# txtfile and aimfile use the variable $name, or the line, to define the text and aim files. Thus, each specimen in filename should not have a suffix. 
	txtfile="$name.txt"
	aimfile="$name.aim"
	# The new .mnc file is sent to /path/to/aim and is given the name $name.mnc. 
	mncfile="/path/to/aim/$name.mnc"	
	# Change the .txt header to UNIX format, then use information within the header to automatically produce .mnc files. 
	dos2unix $txtfile				
	# Search for offset.
	offset_line=`cat $txtfile | grep offset`
	# Code the offset line as arr_off.		
	arr_off=($offset_line)
	# Extract the offset value from the arr_off variable. Note that arr_off[6] may SLIGHTLY differ between studies based on the header information.
	act_offset=${arr_off[6]:0:4}	
	# Search for dim. 
	dimensions=`cat $txtfile | grep -m 1 dim`
	# Code the dim variable as arr_dim
	arr_dim=($dimensions)
	# Extract the x, y, z dimensions from arr_dim. Note that arr_dim[1], arr_dim[2], and arr_dim[3] may also SLIGHTLY differ between studies based on the header information. 
	act_x=${arr_dim[1]}
	act_y=${arr_dim[2]}
	act_z=${arr_dim[3]}
	# Search for element (i.e., resolution). 
	resolution=`cat $txtfile | grep element`
	# Code the element line as arr_res.
	arr_res=($resolution)
	# Extract the x, y, z resolution.
	res_x=${arr_res[4]}
	res_y=${arr_res[5]}
	res_z=${arr_res[6]}
	# Use the parameters defined above to convert the raw data into a .mnc file.
	rawtominc -input $aimfile -short -scan_range -clobber -skip $act_offset -xstep $res_x -ystep $res_y -zstep $res_z -origin 0 0 0 $mncfile $act_z $act_y $act_x
	echo "rawtominc -input "$name.aim" -short -scan_range -clobber -skip $act_offset -xstep $res_x -ystep $res_y -zstep $res_z -origin 0 0 0 "$name.mnc" $act_z $act_y $act_x"
	# Create the montage image for all newly created .mnc files.
	cd "/path/to/aim"		
	qcpost="_QC.png"	
	qcfile="$name$qcpost"	
	labpost="_QC_labeled.png"
	labfile="$name$labpost"	
	mincpik -clobber -scale 20 -triplanar "$name.mnc" "$qcfile"
	convert -label $name "$qcfile" "$labfile"

	montage_cmd+=" /path/to/aim/$labfile"		#Build full montage command
	echo $montage_cmd

done < "$filename"
# Create a montage of the converted images. 
montage_cmd+=" /path/to/aim/<montage.png>"
$montage_cmd 
