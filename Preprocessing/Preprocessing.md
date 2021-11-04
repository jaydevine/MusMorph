#------------------------------------------------------------------------------------------------------------------------
# Preprocessing and initialization instructions.

Preprocessing and initialization can easily be performed on a local machine.

#------------------------------------------------------------------------------------------------------------------------

After downloading the MINC software, add it to your ~/.bashrc script (Linux) or ~/.bash_profile (Mac):  

`nano ~/.bashrc` # scroll to the bottom and add ". /opt/minc/1.9.18/minc-toolkit-config.sh" to call the software in every new Terminal. Ctrl+X+X to save and exit.

Begin by making a directory structure. This structure is important as you will probably want to replicate it on a 
compute cluster for remote processing. Move to /path/to/local/directory and let \<PROJECT\> be your given project name. 

`cd /path/to/local/directory`  

`mkdir -p <PROJECT>/{Scripts,Quality,Source/{Blurred,MNC,Orig,Resample,Tag,XFM},lsq6/{Blurred,MNC,XFM},lsq12/{Blurred,MNC,XFM},nl/{Ana_Test,Blurred,INIT,MNC,XFM}}`

Next we want to convert our set of image volumes to .mnc. You can find conversion commands at http://bic-mni.github.io/man-pages/ and in our GitHub MusMorph "Preprocessing" scripts (https://github.com/jaydevine/MusMorph/tree/main/Preprocessing), such as "AIM_to_MNC.sh", "NIFTI_to_MNC.sh", "TIFF_to_MNC.sh", and "NRRD_to_MNC.py". Most of these scripts require a list of filenames. So, move the original images to /path/to/\<PROJECT\>/Source/Orig and run:

`cd /path/to/<PROJECT>/Source/Orig`
`ls -1 * >> /path/to/<PROJECT>/Source/spec_list.txt` 

then remove the file extensions from the list via sed. If we have .tiff files, we can run:
`sed -i 's/.tiff//g' /path/to/<PROJECT>/Source/spec_list.txt`

Assuming the converted .mnc files are in /path/to/\<PROJECT\>/Source/Orig, we should now perform some preprocessing to prepare our images for spatial normalization. Please see "Downsample_and_Correct.sh" to a) standardize your image dimensions with an atlas (or an arbitrary image) and b) homogenize the intensity profile so that it is not biased by extreme (low or high) values. Further, if your images tend to have a lot of background noise (e.g. if they have been stained with iodine or another contrast agent), consider eliminating that noise with "Threshold.sh". 
  
After preprocessing the image intensities, each image needs to be initialized (i.e. translated and rotated) to a reference image. If your images were scanned in a standard orientation and are roughly aligned, they can be automatically initialized to the reference image. This process is embedded in the full non-linear registration script (e.g. https://github.com/jaydevine/MusMorph/blob/main/Processing/LoRes_Pairwise.py). Skip to the end of this file to setup your cluster for the registrations.

If your images were not scanned in a standard orientation, we need to manually initialize them. To do this, we need to render the image volumes as surfaces and roughly place >=4 sparse landmarks to translate and rotate each image into a reference image space, where we have 1 to 1 voxel correspondences. To expedite this process, you can blur the images, then loop through the blurred images, find a threshold, and automatically generate a surface. Here, your inputs could either be the downsampled and intensity corrected images (*_ds_norm.mnc via Downsample_and_Correct.sh) or the thresholded images (*_thresh.mnc via Threshold.sh):

`for file in *_ds_norm.mnc; do base=$(basename ${file} .mnc); echo ${base}; IMAGE_RES=$(mincinfo ${file} -attvalue zspace:step); BLUR_RES=$(awk "BEGIN {scale=$IMAGE_RES*5; print scale}"); mincblur -clobber -fwhm ${BLUR_RES} ${file} ${base}; STATS=$(mincstats -quiet -biModalT ${base}_blur.mnc); echo ${STATS}; marching_cubes ${base}_blur.mnc ${base}.obj ${STATS}; rm ${base}_blur.mnc; done`

If this thresholding option doesn't work for you, try another method, like Kapur:

`for file in *.mnc; do base=$(basename ${file} .mnc); echo ${base}; IMAGE_RES=$(mincinfo ${file} -attvalue zspace:step); BLUR_RES=$(awk "BEGIN {scale=$IMAGE_RES*5; print scale}"); mincblur -clobber -fwhm ${BLUR_RES} ${file} ${base}; STATS=$(mincstats -quiet -kapur ${base}_blur.mnc); Kapur=$(echo "${STATS}" | tr " " "\n" | sed -n '21p'); marching_cubes ${base}_blur.mnc ${base}.obj ${Kapur}; rm ${base}_blur.mnc; done`

We can then "Display" the .obj surface and place our homologous markers for initialization:

`Display ${Biosample}_ds_norm.obj` # where ${Biosample} is the specimen name in /path/to/<PROJECT>/Source/spec_list.txt.

In the "Display: 3D View" window, consider the following commands: hold right-click to move the entire object, and hold middle scroll to rotate the entire object. Now let's place the initialization landmarks. B: Markers -> Z: Default Size: 1 (lower to 0.2 or so) -> hover over the point at which landmark 1 will be placed and press F: Create Marker. Rinse and repeat. A window called "Display: Objects" with all >=4 markers should be visible. When you're done, press Space: Pop Menu -> T: File -> A: Save Markers as Tag. Let's use the naming convention "${Biosample}.tag", where ${Biosample} is the specimen name in /path/to/<PROJECT>/Source/spec_list.txt. Save the .tag files into \<PROJECT\>/Source/Orig (we will put them into the "Tag" folder later).

Each image .tag file must now be combined with the reference image .tag file to create a two volume .tag file for all pairs. Ideally, your reference image is a well-aligned specimen with sufficient empty space around it (to prevent accidental cropping when you resample). *THIS WOULD BE YOUR ATLAS IMAGE, IF YOU'VE ALREADY CREATED ONE*. If you don't have an atlas, choose an arbitrary reference with the above properties. Use the Tag_Combine.R script (https://github.com/jaydevine/MusMorph/blob/main/Preprocessing/Tag_Combine.R) to combine the initialization landmark files:

`Rscript Tag_Combine.R`

Let's move our original *_landmarks.tag files to a different directory, then use the combined .tag files to create rigid transformation (.xfm) files to resample the target images into the reference space: 

`for file in *to*.tag; do base=$(basename ${file} .tag); echo ${base}; tagtoxfm -lsq6 ${file} ${base}.xfm; done`  

Move the two volume tag files and rename the .xfm files for simplicity:

`mv *to*.tag /path/to/<PROJECT>/Source/Tag`  

`for file in *.xfm; do [ -f "$file" ] || continue; mv $file ${file//Tag_ref_to_}; done` # where ref is your reference name above. 

Use the .xfm matrices to resample the images into the reference space, where -like ${ref}.mnc should be the name of the reference image:  

`for file in *.xfm; do base=$(basename $file .xfm); echo $base; mincresample -like ${ref}.mnc -transformation $file ${base}.mnc ${base}_to_ref.mnc; done`  

After the initialization is done, clean up the directories. Move the intermediate correction files to /path/to/\<PROJECT\>/Source/Resample and the initialized files to /path/to/\<PROJECT\>/Source/MNC. Most of the processing to come will require the original specimen names, so let's just rename:

`mv *_ds_norm.mnc /path/to/<PROJECT>/Source/Resample`
`mv *to_ref.mnc /path/to/<PROJECT>/Source/MNC`
`cd /path/to/<PROJECT>/Source/MNC`  
`for file in *_to_ref.mnc; do [ -f "$file" ] || continue; mv $file ${file//_to_ref}; done`  

If you don't have an atlas, create an initialized average with these images:

`ls -1 *.mnc >> transform_list.txt`  

`mincaverage -2 -clobber -verbose -filelist transform_list.txt LM_average.mnc` # Calling this landmark initialized average LM_average.mnc 

With this average, or with your atlas file, we want to create a mask. The purpose of the mask is to restrict the area with which you compute the registrations; that is, it covers all of the image space/anatomy that actually matters to you. 

`mincmorph -clobber -successive B[lower:upper]DDDDDDDD LM_average.mnc LM_average_mask.mnc`  

where lower and upper are the lower and upper bounds of the densities you wish to include in the mask. "D" refers to dilation and it is used to fill in holes of the mask. Adding more "D"s simply means more dilations. Ideally you have a mask that covers all of the desired anatomy and has no holes. We should now have an atlas (or an initialized average), an atlas mask (or an initilaized average mask), and a set of source images that have been rigidly aligned to the space of this reference image. We want to put these images onto a cluster for parallel registrations, as this is a computationally intense process. To do so, we first ssh into our cluster of choice:

`ssh <USER>@clustername`  

Replicate our local directory structure:

`mkdir -p <PROJECT>/{Scripts,Quality,Source/{Blurred,MNC,Orig,Resample,Tag,XFM},lsq6/{Blurred,MNC,XFM},lsq12/{Blurred,MNC,XFM},nl/{Ana_Test,Blurred,INIT,MNC,XFM}}`

In a separate Terminal, sftp to "put" the atlas/average, mask, and initialized .mnc files into these directories:

`sftp <USER>@clustername`  

`cd /path/to/<PROJECT>/Source/MNC`

`lcd /path/to/<PROJECT>/Source/MNC`  # Adding l before commands in sftp allows you to run stuff locally without exiting the connection.

`put *.mnc`  

Next, follow the non-linear registration Python script (https://github.com/jaydevine/MusMorph/blob/main/Processing/LoRes_Pairwise.py or https://github.com/jaydevine/MusMorph/blob/main/Processing/HiRes_Pairwise.py) to produce a set of Bash (.sh) scripts that will be ran on the cluster. There are Python scripts for pairwise registration (if you've already created/have an atlas) and atlas construction. 

#------------------------------------------------------------------------------------------------------------------------
