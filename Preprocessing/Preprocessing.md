#------------------------------------------------------------------------------------------------------------------------
# Preprocessing and initialization instructions.

Citation:

Preprocessing and initialization can easily be performed on a local machine.

#------------------------------------------------------------------------------------------------------------------------

After downloading the MINC software, add it to your ~/.bashrc script (Linux) or ~/.bash_profile (Mac):  

`nano ~/.bashrc` # scroll to the bottom and add ". /opt/minc/1.9.17/minc-toolkit-config.sh" to call the software in every new Terminal. Ctrl+X+X to save and exit.

Begin by making a directory structure. This structure is important as you will probably want to replicate it on a 
compute cluster for remote processing. Move to a /local/directory/of/choice and let \<PROJECT\> be your given project name. 

`cd /local/directory/of/choice`  

`mkdir -p <PROJECT\>{Scripts,Source/{aim,Blurred,MNC,Orig,Corr,Tag,Tiff,XFM},lsq6/{Blurred,MNC,XFM},lsq12/{Blurred,MNC,XFM},nl/{Ana_Test,Blurred,INIT,MNC,XFM}}`

Next we want to convert our set of image volumes to .mnc. You can find conversion commands at http://bic-mni.github.io/man-pages/ and in our GitHub CranioMorph "Preprocessing" directory (https://github.com/jaydevine/CranioMorph/tree/main/Preprocessing). 

Let's place our converted .mnc files in <PROJECT>/Source/MNC. 
  
If your images were scanned in a standard orientation and are roughly aligned, they can be automatically initialized to the reference image. This process is embedded in the full non-linear registration script (https://github.com/jaydevine/CranioMorph/blob/main/Processing/SyN_Registration.py). Skip to line 83 to setup your cluster for the registrations.

If your images were not scanned in a standard orientation, we need to manually initialize them. To do this, we need to render the image volumes as surfaces and roughly place >=4 landmarks to translate and rotate each image into a reference image space, where we have 1 to 1 voxel correspondences. An interesting way to do this is blur the image (e.g., mincblur -fwhm 0.3, where 0.3 is 300 microns or 10x our original resolution. This homogenizes the intensity profile), then loop through the blurred images and automatically generate a surface:  

`for file in *.mnc; do base=$(basename ${file} .mnc); echo ${base}; mincblur -fwhm 0.3 ${file} ${base}; biModalT=$(mincstats -quiet -biModalT ${base}_blur.mnc); echo ${biModalT}; marching_cubes ${base}_blur.mnc ${base}.obj ${biModalT}; done`

We can then "Display" the .obj surface and place our homologous markers for initialization:

`Display ${base}.obj` # where ${base} is the specimen name above.

In the "Display: 3D View" window, consider the following commands: hold right-click to move the entire object, and hold middle scroll to rotate the entire object. Now let's place the initialization landmarks. B: Markers -> Z: Default Size: 1 (lower to 0.2 or so) -> hover over the point at which landmark 1 will be placed and press F: Create Marker. Rinse and repeat. A window called "Display: Objects" with all >=4 markers should be visible. When you're done, press Space: Pop Menu -> T: File -> A: Save Markers as Tag. Let's use the naming convention "${base}_landmarks.tag" and save them into \<PROJECT\>/Source/MNC (we will put them into the "Tag" folder later).

Each image .tag file must now be combined with the reference image .tag file to create a two volume .tag file for all pairs. Ideally, your reference image is a well-aligned specimen with sufficient empty space around it (to prevent accidental cropping when you resample). *THIS WOULD BE YOUR ATLAS IMAGE, IF YOU'VE ALREADY CREATED ONE*. If you don't have an atlas, choose an arbitrary reference with the above properties. Now, create a specimen list that holds all of your image names:

`ls -1 *.mnc >> spec_list.txt` # then remove the .mnc suffix  

`sed -i 's/.mnc//g' spec_list.txt`  

`mv spec_list.txt <PROJECT>/Source`  

Use the Tag_Combine.R script (https://github.com/jaydevine/CranioMorph/blob/main/Preprocessing/Tag_Combine.R) to combine the initialization landmark files:

`Rscript Tag_Combine.R`  

Let's move our original *_landmarks.tag files to a different directory, then use the combined .tag files to create rigid transformation (.xfm) files to resample the target images into the reference space: 

`for file in *to*.tag; do base=$(basename ${file} .tag); echo ${base}; tagtoxfm -lsq6 ${file} ${base}.xfm; done`  

Move the two volume tag files and rename the .xfm files for simplicity:

`mv *to*.tag <PROJECT>/Source/Tag`  

`for file in *.xfm; do [ -f "$file" ] || continue; mv $file ${file//Tag_ref_to_}; done` # where ref is your reference name above. 

Use the .xfm matrices to resample the images. We can also include an intensity non-uniformity correction and an intensity normalization [0,1] if we want:  

`for file in *.xfm; do base=$(basename $file .xfm); echo $base; mincresample -like ${ref}.mnc -transformation $file ${base}.mnc ${base}_to_ref.mnc; nu_correct ${base}_to_ref.mnc ${base}_corr.mnc; mincnorm -out_floor 0 -out_ceil 1 ${base}_corr.mnc ${base}_norm.mnc; done`  

After the resampling is done, clean up the directories. Move the original files to <PROJECT>/Source/Orig and the corrected *corr* files to \<PROJECT\>/Source/Corr. We want to use the *_norm.mnc images going forward. Most of the processing to come will require the original specimen names, so let's just rename:

`for file in *norm.mnc; do [ -f "$file" ] || continue; mv $file ${file//_norm}; done`  

If you don't have an atlas, create an initialized average with these images:

`ls -1 *.mnc >> transform_list.txt`  

`mincaverage -2 -clobber -verbose -filelist transform_list.txt LM_average.mnc` # Calling this landmark initialized average LM_average.mnc 

With this average, or with your atlas file, we want to create a mask. The purpose of the mask is to restrict the area with which you compute the registrations; that is, it covers all of the image space/anatomy that actually matters to you. 

`mincmorph -clobber -successive B[lower:upper]DDDDDDDD LM_average.mnc LM_average_mask.mnc`  

where lower and upper are the lower and upper bounds of the densities you wish to include in the mask. "D" refers to dilation and it is used to fill in holes of the mask. Adding more "D"s simply means more dilations. Ideally you have a mask that covers all of the desired anatomy and has no holes. If you have an atlas, just change LM_average.mnc to the atlas name. We use the name NL_4_average.mnc in our scripts.  

We now have an atlas (or an initialized average), an atlas mask (or an initilaized average mask), and a set of source images that have been rigidly aligned to the space of this reference image. We want to put these images onto a cluster for parallel registrations, as this is a computationally intense process. To do so, we first ssh into our cluster of choice:

`ssh <USER>@clustername`  

Replicate our local directory structure:

`mkdir -p <PROJECT>/{Scripts,Source/{aim,Blurred,MNC,Orig,Corr,Tag,Tiff,XFM},lsq6/{Blurred,MNC,XFM},lsq12/{Blurred,MNC,XFM},nl/{Ana_Test,Blurred,INIT,MNC,XFM}}`  

In a separate Terminal, sftp to "put" the atlas/average, mask, and initialized .mnc files into these directories:

`sftp <USER>@clustername`  

`cd <PROJECT>/Source/MNC`

`lcd <PROJECT>/Source/MNC`  # Adding l before commands in sftp allows you to run stuff locally without exiting the connection.

`put *.mnc`  

Next, follow the non-linear registration Python script (https://github.com/jaydevine/CranioMorph/blob/main/Processing/SyN_Registration.py) to produce a set of Bash (.sh) scripts that will be ran on the cluster. There are Python scripts for pairwise registration (if you've already created/have an atlas) and atlas construction. 

#------------------------------------------------------------------------------------------------------------------------
