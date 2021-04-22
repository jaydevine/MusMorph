# Python script to generate a group-wise atlas. It will generate a series of Bash scripts that will register your images to one another so as to create an iteratively evolving
# average. This should happen on a compute cluster using the MINC toolkit module. Note that the parameters used throughout this script have been adapted for isotropic 35 micron uCT volumes.
# You'll need to adapt the blurring and registration values to your data.

# Citation: Percival, C.J., Devine, J., Darwin, B.C., Liu, W., van Eede, M., Henkelman, R.M. and Hallgrimsson, B., 2019. The effect of automated landmark identification on morphometric analyses. J Anat (2019). https://doi.org/10.1111/joa.12973
# Citation: Devine, J., Aponte, J.D., Katz, D.C. et al. A Registration and Deep Learning Approach to Automated Landmark Detection for Geometric Morphometrics. Evol Biol (2020). https://doi.org/10.1007/s11692-020-09508-8
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Import packages.
import os
import csv
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Some important notes:
# 1) Your local and remote directories should match the compute cluster paths below. Replace <PROJECT> with your project name;
# 2) Your local specimen lists must be called spec_list.txt (all specimens), spec_list2.txt (representative subset), and spec_list3.txt (remainder specimens, or all specimens - subset specimens).
# 3) Your initialized source images MUST be called $spec.mnc, where $spec is the exact name of the specimen annotated in spec_list.txt;
# 4) Your initial average and average mask must be called LM_average.mnc and LM_average_mask.mnc, respectively;
# 5) The initialized source images, average, and average mask must be sftp'd into your remote ~/<PROJECT>/Source/MNC directory on the cluster before any analyses can begin.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Define local working directory.
os.chdir("/path/to/project/")
# Define list of all specimens.  This should should be a single column of your specimen names (without the .mnc suffix). Make sure there aren't any hidden characters in the list (e.g., a space beside a name).
All_Specimens = "/path/to/project/spec_list.txt"
# Define list of subset (N=25) specimens. Again, the .txt file should be a single column of names without hidden characters.
Subset_Specimens = "/path/to/project/spec_list2.txt"
# Define list of remainder specimens; that is, every specimen not included in the representative training subset. The .txt file should be a single column of names without hidden characters.
Remainder_Specimens = "/path/to/project/spec_list3.txt"

# Create remote directory structure that matches your local structure. E.g.:
# mkdir -p <PROJECT\>{Scripts,Source/{aim,Blurred,MNC,Orig,Corr,Tag,Tiff,XFM},lsq6/{Blurred,MNC,XFM},lsq12/{Blurred,MNC,XFM},nl/{Ana_Test,Blurred,INIT,MNC,XFM}}

# Define remote directories (i.e., your compute cluster paths). We use the notation below because it is commonly seen in MINC.
Scripts_path = "~/<PROJECT>/Scripts/"
Source_XFM_path = "~/<PROJECT>/Source/XFM/"
Source_MNC_path = "~/<PROJECT>/Source/MNC/"
lsq6_Blurred_path = "~/<PROJECT>/lsq6/Blurred/"
lsq6_XFM_path = "~/<PROJECT>/lsq6/XFM/"
lsq6_MNC_path = "~/<PROJECT>/lsq6/MNC/"
lsq12_Blurred_path = "~/<PROJECT>/lsq12/Blurred/"
lsq12_XFM_path = "~/<PROJECT>/lsq12/XFM/"
lsq12_MNC_path = "~/<PROJECT>/lsq12/MNC/"
nl_Init_path = "~/<PROJECT>/nl/INIT/"
nl_Blurred_path = "~/<PROJECT>/nl/Blurred/"
nl_XFM_path = "~/<PROJECT>/nl/XFM/"
nl_MNC_path = "~/<PROJECT>/nl/MNC/"

# Define average files.
LM_Avg = "~/<PROJECT>/Source/MNC/LM_average.mnc"
LM_Avg_Mask = "~/<PROJECT>/Source/MNC/LM_average_mask.mnc"
lsq6_Avg = "~/<PROJECT>/lsq6/<PROJECT>_lsq6_average.mnc"
lsq12_Avg = "~/<PROJECT>/lsq12/<PROJECT>_lsq12_average.mnc"
lsq12_Subset_Avg = "~/<PROJECT>/lsq12/<PROJECT>_lsq12_subset_average.mnc"
nl_1_Avg = "~/<PROJECT>/nl/MNC/NL_1_average.mnc"
nl_2_Avg = "~/<PROJECT>/nl/MNC/NL_2_average.mnc"
nl_3_Avg = "~/<PROJECT>/nl/MNC/NL_3_average.mnc"
nl_4_Avg = "~/<PROJECT>/nl/MNC/NL_4_average.mnc"

# Define blur files without "_blur" suffix.
LM_Avg_352 = "~/<PROJECT>/Source/MNC/LM_average_352"
LM_Avg_176 = "~/<PROJECT>/Source/MNC/LM_average_176"
LM_Avg_098 = "~/<PROJECT>/Source/MNC/LM_average_098"
LM_Avg_078 = "~/<PROJECT>/Source/MNC/LM_average_078"
LM_Avg_064 = "~/<PROJECT>/Source/MNC/LM_average_064"
LM_Avg_050 = "~/<PROJECT>/Source/MNC/LM_average_050"
LM_Avg_Mask_1400 = "~/<PROJECT>/nl/INIT/LM_average_mask_1400"
LM_Avg_Mask_1000 = "~/<PROJECT>/nl/INIT/LM_average_mask_1000"
LM_Avg_Mask_700 = "~/<PROJECT>/nl/INIT/LM_average_mask_700"
LM_Avg_Mask_400 = "~/<PROJECT>/nl/INIT/LM_average_mask_400"
LM_Avg_Mask_352 = "~/<PROJECT>/Source/MNC/LM_average_mask_352"
LM_Avg_Mask_176 = "~/<PROJECT>/Source/MNC/LM_average_mask_176"
LM_Avg_Mask_098 = "~/<PROJECT>/Source/MNC/LM_average_mask_098"
LM_Avg_Mask_078 = "~/<PROJECT>/Source/MNC/LM_average_mask_078"
LM_Avg_Mask_064 = "~/<PROJECT>/Source/MNC/LM_average_mask_064"
LM_Avg_Mask_050 = "~/<PROJECT>/Source/MNC/LM_average_mask_050"
lsq12_Avg_1400 = "~/<PROJECT>/nl/INIT/<PROJECT>_lsq12_average_1400"
lsq12_Subset_Avg_098 = "~/<PROJECT>/lsq12/Blurred/<PROJECT>_lsq12_subset_average_098"
lsq12_Subset_Avg_064 = "~/<PROJECT>/lsq12/Blurred/<PROJECT>_lsq12_subset_average_064"
lsq12_Subset_Avg_050 = "~/<PROJECT>/lsq12/Blurred/<PROJECT>_lsq12_subset_average_050"
nl_1_Avg_1000 = "~/<PROJECT>/nl/INIT/NL_1_average_1000"
nl_2_Avg_700 = "~/<PROJECT>/nl/INIT/NL_2_average_700"
nl_3_Avg_400 = "~/<PROJECT>/nl/INIT/NL_3_average_400"

# Define blur files with "_blur" suffix.
LM_Avg_352_Blur = "~/<PROJECT>/Source/MNC/LM_average_352_blur.mnc"
LM_Avg_176_Blur = "~/<PROJECT>/Source/MNC/LM_average_176_blur.mnc"
LM_Avg_098_Blur = "~/<PROJECT>/Source/MNC/LM_average_098_blur.mnc"
LM_Avg_078_Blur = "~/<PROJECT>/Source/MNC/LM_average_078_blur.mnc"
LM_Avg_064_Blur = "~/<PROJECT>/Source/MNC/LM_average_064_blur.mnc"
LM_Avg_050_Blur = "~/<PROJECT>/Source/MNC/LM_average_050_blur.mnc"
LM_Avg_Mask_1400_Blur = "~/<PROJECT>/nl/INIT/LM_average_mask_1400_blur.mnc"
LM_Avg_Mask_1000_Blur = "~/<PROJECT>/nl/INIT/LM_average_mask_1000_blur.mnc"
LM_Avg_Mask_700_Blur = "~/<PROJECT>/nl/INIT/LM_average_mask_700_blur.mnc"
LM_Avg_Mask_400_Blur = "~/<PROJECT>/nl/INIT/LM_average_mask_400_blur.mnc"
LM_Avg_Mask_352_Blur = "~/<PROJECT>/Source/MNC/LM_average_mask_352_blur.mnc"
LM_Avg_Mask_176_Blur = "~/<PROJECT>/Source/MNC/LM_average_mask_176_blur.mnc"
LM_Avg_Mask_098_Blur = "~/<PROJECT>/Source/MNC/LM_average_mask_098_blur.mnc"
LM_Avg_Mask_078_Blur = "~/<PROJECT>/Source/MNC/LM_average_mask_078_blur.mnc"
LM_Avg_Mask_064_Blur = "~/<PROJECT>/Source/MNC/LM_average_mask_064_blur.mnc"
LM_Avg_Mask_050_Blur = "~/<PROJECT>/Source/MNC/LM_average_mask_050_blur.mnc"
lsq12_Avg_1400_Blur = "~/<PROJECT>/nl/INIT/<PROJECT>_lsq12_average_1400_blur.mnc"
lsq12_Subset_Avg_098_Blur = "~/<PROJECT>/lsq12/Blurred/<PROJECT>_lsq12_subset_average_098_blur.mnc"
lsq12_Subset_Avg_064_Blur = "~/<PROJECT>/lsq12/Blurred/<PROJECT>_lsq12_subset_average_064_blur.mnc"
lsq12_Subset_Avg_050_Blur = "~/<PROJECT>/lsq12/Blurred/<PROJECT>_lsq12_subset_average_050_blur.mnc"
nl_1_Avg_1000_Blur = "~/<PROJECT>/nl/INIT/NL_1_average_1000_blur.mnc"
nl_2_Avg_700_Blur = "~/<PROJECT>/nl/INIT/NL_2_average_700_blur.mnc"
nl_3_Avg_400_Blur = "~/<PROJECT>/nl/INIT/NL_3_average_400_blur.mnc"

# Open and read ('r') the all specimen list.
Specimen_List=open(All_Specimens,'r')
# Read specimen list as a single string.
Specimens=Specimen_List.read()
# Split the specimens by line to obtain a vector of specimen IDs.
Specimen_IDs=Specimens.split('\n')
# Remove the last blank entry caused by the final \n.
del Specimen_IDs[-1]
# Define the length of the specimen list.
Specimen_List_Length=len(Specimen_IDs)
# Divide the length of the list by the same number.
Specimen_Group=int(Specimen_List_Length/Specimen_List_Length)
# Calculate upper limit of specimen list to use in for loop sequences.
Specimen_Upper=(Specimen_List_Length*Specimen_List_Length)-1
# Close the specimen list.
Specimen_List.close()

# Open and read ('r') the subset specimen list.
Subset_Specimen_List=open(Subset_Specimens,'r')
# Read specimen list as a single string.
Subset_Specimens=Subset_Specimen_List.read()
# Split the specimens by line to obtain a vector of specimen IDs.
Subset_Specimen_IDs=Subset_Specimens.split('\n')
# Remove the last blank entry caused by the final \n.
del Subset_Specimen_IDs[-1]
# Define the length of the subset specimen list.
Subset_Specimen_List_Length=len(Subset_Specimen_IDs)
# Divide the length of the list by the same number.
Subset_Specimen_Group=int(Subset_Specimen_List_Length/Subset_Specimen_List_Length)
# Calculate upper limit of subset specimen list to use in for loop sequences.
Subset_Specimen_Upper=(Subset_Specimen_List_Length*Subset_Specimen_List_Length)-1
# Close the specimen list.
Subset_Specimen_List.close()

# Open and read ('r') the remainder specimen list.
Remainder_Specimen_List=open(Remainder_Specimens,'r')
# Read specimen list as a single string.
Remainder_Specimens=Remainder_Specimen_List.read()
# Split the specimens by line to obtain a vector of specimen IDs.
Remainder_Specimen_IDs=Remainder_Specimens.split('\n')
# Remove the last blank entry caused by the final \n.
del Remainder_Specimen_IDs[-1]
# Define the length of the remainder specimen list.
Remainder_Specimen_List_Length=len(Remainder_Specimen_IDs)
# Divide the length of the list by the same number.
Remainder_Specimen_Group=int(Remainder_Specimen_List_Length/Remainder_Specimen_List_Length)
# Calculate upper limit of remainder specimen list to use in for loop sequences.
Remainder_Specimen_Upper=(Specimen_List_Length-Subset_Specimen_List_Length)-1
# Close the specimen list.
Remainder_Specimen_List.close()

# Code the strings for iterative blurring via mincblur. -clobber overwrites existing files; -no apodize turns off apodization, which is designed to reduce diffraction edge effects (e.g., detector noise);
# -gradient calculates the change in intensity of a single pixel in the source image to the target image; -fwhm stands for full-width at half-maximum. In other words, what we want to do is convolve a
# "smoothing kernel", or Gaussian function, over an input volume in order to average neighboring points. The full-width at half-maximum describes the width of the Gaussian function at half of its peak to the left and right;
MNC_Blur = "mincblur -clobber -no_apodize -gradient -fwhm "

# Code the hierarchical registration strings which call upon the minctracc command. -clobber overwrites existing files; -xcorr stands for cross-correlation, which is the similarity metric to be optimized (maximized);
# -lsq6 indicates that we want perform a rigid body transformation with six degrees of freedom (translation (z,y,x) and rotation (z,y,x)); -lsq12 indicates that we want to perform a 12-parameter affine transformation
# with twelve degrees of freedom (translation (z,y,x), rotation (z,y,x), scale (z,y,x), and shear (z,y,x)); -w_translations/rotations/scales/shear optimization weights along z,y,x; -step is the z,y,x resolution;
# -simplex is the optimizer; -tol is the value at which the optimization stops.
lsq6_Register_352_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.352 0.352 0.352 -simplex 0.78 -use_simplex -tol 0.0001 "
lsq6_Register_176_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.176 0.176 0.176 -simplex 0.54 -use_simplex -tol 0.0001 "
lsq6_Register_078_Blur = "minctracc -clobber -xcorr -lsq6 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.078 0.078 0.078 -simplex 0.32 -use_simplex -tol 0.0001 "
lsq12_Register_098_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.098 0.098 0.098 -simplex 0.980 -use_simplex -tol 0.0001 "
lsq12_Register_064_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.064 0.064 0.064 -simplex 0.490 -use_simplex -tol 0.0001 "
lsq12_Register_050_Blur = "minctracc -clobber -xcorr -lsq12 -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.050 0.050 0.050 -simplex 0.333 -use_simplex -tol 0.0001 "
nl_1_Register_1400_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 1.4 1.4 1.4 -simplex 3.5 -use_simplex -tol 0.0001 "
nl_1_Register_1400_Blur_End = "-iterations 40 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 4.2 4.2 4.2 -max_def_magnitude 1 -debug -xcorr -identity "
nl_2_Register_1000_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 1.0 1.0 1.0 -simplex 3.5 -use_simplex -tol 0.0001 "
nl_2_Register_1000_Blur_End = "-iterations 20 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 3.0 3.0 3.0 -max_def_magnitude 1 -debug -xcorr -transform "
nl_3_Register_700_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.7 0.7 0.7 -simplex 3.5 -use_simplex -tol 0.0001 "
nl_3_Register_700_Blur_End = "-iterations 15 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 2.1 2.1 2.1 -max_def_magnitude 1 -debug -xcorr -transform "
nl_4_Register_400_Blur_Begin = "minctracc -clobber -xcorr -w_translations 0.4 0.4 0.4 -w_rotations 0.0174533 0.0174533 0.0174533 -w_scales 0.02 0.02 0.02 -w_shear 0.02 0.02 0.02 -step 0.4 0.4 0.4 -simplex 3.5 -use_simplex -tol 0.0001 "
nl_4_Register_400_Blur_End = "-iterations 15 -similarity 0.8 -weight 0.8 -stiffness 0.98 -nonlinear corrcoeff -sub_lattice 6 -lattice_diameter 1.2 1.2 1.2 -max_def_magnitude 1 -debug -xcorr -transform "

# Beginning of mincaverage command to which .mnc files will be added.
lsq6_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
lsq12_Subset_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
lsq12_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_1_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_2_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_3_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "
nl_4_MNC_Avg = "mincaverage -clobber -2 -filetype -nonormalize "

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Begin writing .sh scripts that will be submitted to the cluster.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 6-parameter (translation (z,y,x), rotation (z,y,x)) optimal rigid body registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Open a file to write to; 'a' for append; lsq6_First is the first 6-parameter .sh script to submit, because it blurs the intended target (i.e., the landmark initialized average) as well as a mask of equivalent resolution to constrain our computation.
lsq6_First = open("lsq6_First.sh",'a')
# Write standard .sh header. This header is needed for SLURM job submission.
lsq6_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=05:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
# Write commands to blur LM_average and LM_average_mask with isotropic blurring kernels of 352 microns, 176 microns, and 78 microns. These blur values should be decided upon with respect to the original resolution of the image.
# Here, we're assuming 35 micron resolution.
lsq6_First.write(MNC_Blur + "0.352 " + LM_Avg + " " + LM_Avg_352 + "\n")
lsq6_First.write(MNC_Blur + "0.176 " + LM_Avg + " " + LM_Avg_176 + "\n")
lsq6_First.write(MNC_Blur + "0.078 " + LM_Avg + " " + LM_Avg_078 + "\n")
lsq6_First.write(MNC_Blur + "0.352 " + LM_Avg_Mask + " " + LM_Avg_Mask_352 + "\n")
lsq6_First.write(MNC_Blur + "0.176 " + LM_Avg_Mask + " " + LM_Avg_Mask_176 + "\n")
lsq6_First.write(MNC_Blur + "0.078 " + LM_Avg_Mask + " " + LM_Avg_Mask_078 + "\n\n")
lsq6_First.write("echo \"The job ended at $(date).\"")
# Close the file.
lsq6_First.close()

# Begin a for loop to blur all landmark initialized source files, register them to LM_Average, and resample each image into the new translation and rotation invariant space.
# Note that we ideally want to resample the LM initialized images, rather than the original .mnc images. Hence, the initialization .xfm is not included in the concatenation.
# Begin a counter.
lsq6_Counter=0
for SpecID in Specimen_IDs:
	# Add 1 to the counter for every new file in the loop.
	lsq6_Counter += 1
	# Open a file to write to; 'a' for append.
	lsq6_Second = open("lsq6_Second_" + str(lsq6_Counter) + ".sh",'a')
	# Add header.
	lsq6_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	lsq6_Second.write("echo \"Begin the optimized 6-parameter registration for " + SpecID + ".\"\n\n")
	# Blur each image, as done with the average and average mask, with a 0.352, 0.176, and 0.078 isotropic Gaussian blurring kernel. These blur values should be decided upon with respect to the original resolution of the image.
	lsq6_Second.write(MNC_Blur + "0.352 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_352\n")
	lsq6_Second.write(MNC_Blur + "0.176 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_176\n")
	lsq6_Second.write(MNC_Blur + "0.078 " + Source_MNC_path + SpecID + ".mnc " + lsq6_Blurred_path + SpecID + "_078\n")
	# Call registration strings. We begin with the most blurred (e.g., 0.352) image. -model_mask specifies the mask we wish to use. Note that we use a mask with the same amount of blurring;
	# -identity specifies an identity matrix that initializes the transformation matrix. Upon specifying a transformation matrix, we extract the relevant transformation parameters (here, rotation and translation)
	# and optimize them to find the best transformation; -transformation specifies a file giving a previous source to target mapping, which is used as the new coordinate starting point for the optimization.
	lsq6_Second.write(lsq6_Register_352_Blur + lsq6_Blurred_path + SpecID + "_352_blur.mnc " + LM_Avg_352_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_0.xfm -model_mask " + LM_Avg_Mask_352_Blur + " -identity\n")
	lsq6_Second.write(lsq6_Register_176_Blur + lsq6_Blurred_path + SpecID + "_176_blur.mnc " + LM_Avg_176_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_1.xfm -model_mask " + LM_Avg_Mask_176_Blur + " -transformation " + lsq6_XFM_path + SpecID + "_lsq6_0.xfm\n")
	lsq6_Second.write(lsq6_Register_078_Blur + lsq6_Blurred_path + SpecID + "_078_blur.mnc " + LM_Avg_078_Blur + " " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm -model_mask " + LM_Avg_Mask_078_Blur + " -transformation " + lsq6_XFM_path + SpecID + "_lsq6_1.xfm\n")
	# Resample the original image into the rotation and translation invariant space using the concatenated transformation. Be mindful of your "original" images and their naming convention.
	lsq6_Second.write("mincresample -like " + LM_Avg + " -clobber -transformation " + lsq6_XFM_path + SpecID + "_lsq6_2.xfm " + Source_MNC_path + SpecID + ".mnc " + lsq6_MNC_path + SpecID + "_lsq6.mnc\n\n")
	lsq6_Second.write("echo \"The job ended at $(date).\"")
	# Close the 6-parameter blur/register file.
	lsq6_Second.close()

# Open a file to write to; 'a' for append; lsq6_Third is the third and final stage of 6-parameter .sh scripts to submit.
lsq6_Third = open("lsq6_Third.sh",'a')
# Add header.
lsq6_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
lsq6_Third.write("echo \"All lsq6 files are being averaged.\"\n")
# Add _lsq6.mnc files to MNC_Avg string.
for SpecID in Specimen_IDs:
	lsq6_MNC_Avg += lsq6_MNC_path + SpecID + "_lsq6.mnc "
lsq6_Third.write(lsq6_MNC_Avg + lsq6_Avg + "\n\n")
lsq6_Third.write("echo \"The job ended at $(date).\"")
# Close the 6-parameter average file.
lsq6_Third.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 12-parameter (translation (z,y,x), rotation (z,y,x), scale (z,y,x), shear (z,y,x)) optimized affine registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Open file to write to; 'a' for append.
lsq12_First = open("lsq12_First.sh",'a')
# Add header.
lsq12_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
lsq12_First.write("echo \"We are blurring LM_average and LM_average_mask.\"\n")
lsq12_First.write(MNC_Blur + "0.098 " + LM_Avg + " " + LM_Avg_098 + "\n")
lsq12_First.write(MNC_Blur + "0.064 " + LM_Avg + " " + LM_Avg_064 + "\n")
lsq12_First.write(MNC_Blur + "0.050 " + LM_Avg + " " + LM_Avg_050 + "\n")
lsq12_First.write(MNC_Blur + "0.098 " + LM_Avg_Mask + " " + LM_Avg_Mask_098 + "\n")
lsq12_First.write(MNC_Blur + "0.064 " + LM_Avg_Mask + " " + LM_Avg_Mask_064 + "\n")
lsq12_First.write(MNC_Blur + "0.050 " + LM_Avg_Mask + " " + LM_Avg_Mask_050 + "\n\n")
lsq12_First.write("echo \"The job ended at $(date).\"")
# Close the average blur file.
lsq12_First.close()

# Write commands to blur all specimens with isotropic blurring kernels equal in size to those used in lsq12_First.
# Begin a counter.
lsq12_Counter=0
for SpecID in Specimen_IDs:
	# Add 1 to the counter for every new file in the loop.
	lsq12_Counter += 1
	# Open a file to write to; 'a' for append.
	lsq12_Second = open("lsq12_Second_" + str(lsq12_Counter) + ".sh",'a')
	# Add header.
	lsq12_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	lsq12_Second.write("echo \"We are blurring " + SpecID + ".\"\n")
	# Blur the previously created lsq6 images, as done with the average and average mask, with a 0.098, 0.064, and 0.050 isotropic Gaussian blurring kernel. These blur values should be decided upon with respect to the original resolution of the image.
	lsq12_Second.write(MNC_Blur + "0.098 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_098\n")
	lsq12_Second.write(MNC_Blur + "0.064 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_064\n")
	lsq12_Second.write(MNC_Blur + "0.050 " + lsq6_MNC_path + SpecID + "_lsq6.mnc " + lsq12_Blurred_path + SpecID + "_050\n\n")
	lsq12_Second.write("echo \"The job ended at $(date).\"")
	# Close the 12-parameter blur file.
	lsq12_Second.close()

# Create a single big .sh file containing all of the 12-parameter pairwise registration commands.
# Open a file to write to; 'a' for append.
lsq12_Third = open("lsq12_Temp_Big.sh",'a')
for Subset_SpecID in Subset_Specimen_IDs:
	for Subset_SpecID2 in Subset_Specimen_IDs:
		# Add header.
		lsq12_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=10000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
		# Call the registration strings. We begin with the most blurred (e.g., 0.098 microns) image. -model_mask specifies the mask we wish to use. Note that we use a -model_mask with the same amount of blurring to constrain our computation.
		# -identity specifies an identity matrix that initializes the transformation matrix. Upon specifying a transformation matrix, we extract the relevant transformation parameters (here, rotation and translation) and optimize them to find the
		# best transformation; -transform specifies a file giving a previous source to target mapping, which is used as the new coordinate starting point for the optimization.
		lsq12_Third.write(lsq12_Register_098_Blur + lsq12_Blurred_path + Subset_SpecID + "_098_blur.mnc " + lsq12_Blurred_path + Subset_SpecID2 + "_098_blur.mnc " + lsq12_XFM_path + Subset_SpecID + "_to_" + Subset_SpecID2 + "_lsq12_0.xfm -model_mask " + LM_Avg_Mask_098_Blur + " -identity\n")
		lsq12_Third.write(lsq12_Register_064_Blur + lsq12_Blurred_path + Subset_SpecID + "_064_blur.mnc " + lsq12_Blurred_path + Subset_SpecID2 + "_064_blur.mnc " + lsq12_XFM_path + Subset_SpecID + "_to_" + Subset_SpecID2 + "_lsq12_1.xfm -model_mask " + LM_Avg_Mask_064_Blur + " -transform " + lsq12_XFM_path + Subset_SpecID + "_to_" + Subset_SpecID2 + "_lsq12_0.xfm\n")
		lsq12_Third.write(lsq12_Register_050_Blur + lsq12_Blurred_path + Subset_SpecID + "_050_blur.mnc " + lsq12_Blurred_path + Subset_SpecID2 + "_050_blur.mnc " + lsq12_XFM_path + Subset_SpecID + "_to_" + Subset_SpecID2 + "_lsq12_2.xfm -model_mask " + LM_Avg_Mask_050_Blur + " -transform " + lsq12_XFM_path + Subset_SpecID + "_to_" + Subset_SpecID2 + "_lsq12_1.xfm\n")
		lsq12_Third.write("echo \"The job ended at $(date).\"\n")
# Close the 12-parameter registration file.
lsq12_Third.close()

# Divide the lsq12_Temp_Big.sh file into a series of small lsq12_Third_*.sh files.
# lines_per_file is equal to the number of lines to divide each script into. Note that this MAY vary depending on the cluster and job requirements you're using!
lines_per_file = 15
# Give the smallfile variable null behavior.
smallfile = None
# Open the previously created lsq12_Temp_Big.sh file, refer to it as the bigfile object, and split it into 18 line chunks.
with open("lsq12_Temp_Big.sh") as bigfile:
	for lineno, line in enumerate(bigfile):
		if lineno % lines_per_file == 0:
			if smallfile:
				smallfile.close()
			small_filename = "lsq12_Third_" + str(int(lineno/15)) + ".sh"
			smallfile = open(small_filename, "w")
		smallfile.write(line)
	if smallfile:
			smallfile.close()

# Range should be equal to the number of subset specimens, because we want a single file for each specimen.
for Element in list(range(Subset_Specimen_List_Length)):
	# Open a file to write to; 'a' for append.
	lsq12_Fourth = open("lsq12_Fourth_" + str(Element) + ".sh",'a')
	# Add header.
	lsq12_Fourth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=10000M\n#SBATCH --time=05:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	# Start XFM_Avg string for each specimen.
	XFM_Avg ="xfmavg -verbose -clobber "
	for Subset_SpecID in Subset_Specimen_IDs[(Subset_Specimen_Group*Element):(Subset_Specimen_Group*(Element+1))]:
		for Subset_SpecID2 in Subset_Specimen_IDs:
			XFM_Avg += lsq12_XFM_path + Subset_SpecID + "_to_" + Subset_SpecID2 + "_lsq12_2.xfm "
		# Average the added $spec_to_$spec2_lsq12_2.xfm files in the form of $spec_lsq12_AVG.xfm.
		lsq12_Fourth.write(XFM_Avg + lsq12_XFM_path + Subset_SpecID + "_lsq12_AVG.xfm\n")
		# Concatenate .xfm files.
		lsq12_Fourth.write("xfmconcat -clobber " + lsq6_XFM_path + Subset_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Subset_SpecID + "_lsq12_AVG.xfm " + lsq12_XFM_path + Subset_SpecID + "_origtolsq12.xfm\n")
		# Resample source image into 12-parameter space with concatenated .xfm.
		lsq12_Fourth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + lsq12_XFM_path + Subset_SpecID + "_origtolsq12.xfm " + Source_MNC_path + Subset_SpecID + ".mnc " + lsq12_MNC_path + Subset_SpecID + "_lsq12.mnc\n\n")
	lsq12_Fourth.write("echo \"The job ended at $(date).\"")
	# Close the xfmconcat and resample file.
	lsq12_Fourth.close()

# Create .mnc average script for subset specimens.
# Open a file to write to; 'a' for append.
lsq12_Fifth = open("lsq12_Fifth.sh",'a')
# Add header.
lsq12_Fifth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
lsq12_Fifth.write("echo \"All subset lsq12 files are being averaged.\"\n")
for Subset_SpecID in Subset_Specimen_IDs:
	# Add the new $spec_lsq12.mnc files to the Avg_String variable.
	lsq12_Subset_MNC_Avg += lsq12_MNC_path + Subset_SpecID + "_lsq12.mnc "
lsq12_Fifth.write(lsq12_Subset_MNC_Avg + lsq12_Subset_Avg + "\n")
lsq12_Fifth.write(MNC_Blur + "0.098 " + lsq12_Subset_Avg + " " + lsq12_Subset_Avg_098 + "\n")
lsq12_Fifth.write(MNC_Blur + "0.064 " + lsq12_Subset_Avg + " " + lsq12_Subset_Avg_064 + "\n")
lsq12_Fifth.write(MNC_Blur + "0.050 " + lsq12_Subset_Avg + " " + lsq12_Subset_Avg_050 + "\n\n")
lsq12_Fifth.write("echo \"The job ended at $(date).\"")
# Close the average file.
lsq12_Fifth.close()

# Create a single .sh file containing all of the 12-parameter transformations between the remainder specimen list and the subset average.
# Open a file to write to; 'a' for append.
lsq12_Sixth = open("lsq12_Temp_Big_Remainder.sh",'a')
for Remainder_SpecID in Remainder_Specimen_IDs:
	# Add header.
	lsq12_Sixth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=10000M\n#SBATCH --time=07:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	# Registration strings.
	lsq12_Sixth.write(lsq12_Register_098_Blur + lsq12_Blurred_path + Remainder_SpecID + "_098_blur.mnc " + lsq12_Subset_Avg_098_Blur + " " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_0.xfm -model_mask " + LM_Avg_Mask_098_Blur + " -identity\n")
	lsq12_Sixth.write(lsq12_Register_064_Blur + lsq12_Blurred_path + Remainder_SpecID + "_064_blur.mnc " + lsq12_Subset_Avg_064_Blur + " " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_1.xfm -model_mask " + LM_Avg_Mask_064_Blur + " -transform " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_0.xfm\n")
	lsq12_Sixth.write(lsq12_Register_050_Blur + lsq12_Blurred_path + Remainder_SpecID + "_050_blur.mnc " + lsq12_Subset_Avg_050_Blur + " " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_2.xfm -model_mask " + LM_Avg_Mask_050_Blur + " -transform " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_1.xfm\n")
	lsq12_Sixth.write("echo \"The job ended at $(date).\"\n")
	# Close the 12-parameter registration file.
lsq12_Sixth.close()

# Open the previously created lsq12_Temp_Big.sh file, refer to it as the bigfile object, and split it into 18 line chunks.
with open("lsq12_Temp_Big_Remainder.sh") as bigfile:
	for lineno, line in enumerate(bigfile):
		if lineno % lines_per_file == 0:
			if smallfile:
				smallfile.close()
			small_filename = "lsq12_Sixth_" + str(int(lineno/15)) + ".sh"
			smallfile = open(small_filename, "w")
		smallfile.write(line)
	if smallfile:
			smallfile.close()

# Range should be equal to the number of subset specimens, because we want a single file for each specimen.
for Element in list(range(Remainder_Specimen_List_Length)):
	# Open a file to write to; 'a' for append.
	lsq12_Seventh = open("lsq12_Seventh_" + str(Element) + ".sh",'a')
	# Add header.
	lsq12_Seventh.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=10000M\n#SBATCH --time=05:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Remainder_SpecID in Remainder_Specimen_IDs[(Remainder_Specimen_Group*Element):(Remainder_Specimen_Group*(Element+1))]:
		# Concatenate .xfm files.
		lsq12_Seventh.write("xfmconcat -clobber " + lsq6_XFM_path + Remainder_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_2.xfm " + lsq12_XFM_path + Remainder_SpecID + "_origtolsq12.xfm\n")
		# Resample source image into 12-parameter space with concatenated .xfm.
		lsq12_Seventh.write("mincresample -like " + LM_Avg + " -clobber -transformation " + lsq12_XFM_path + Remainder_SpecID + "_origtolsq12.xfm " + Source_MNC_path + Remainder_SpecID + ".mnc " + lsq12_MNC_path + Remainder_SpecID + "_lsq12.mnc\n\n")
	lsq12_Seventh.write("echo \"The job ended at $(date).\"")
	# Close the xfmconcat and resample file.
	lsq12_Seventh.close()

# Create .mnc average script for both the subset and remainder specimens.
# Open a file to write to; 'a' for append.
lsq12_Eighth = open("lsq12_Eighth.sh",'a')
# Add header.
lsq12_Eighth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=05:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
lsq12_Eighth.write("echo \"All lsq12 files are being averaged.\"\n")
for SpecID in Specimen_IDs:
	lsq12_MNC_Avg += lsq12_MNC_path + SpecID + "_lsq12.mnc "
lsq12_Eighth.write(lsq12_MNC_Avg + lsq12_Avg + "\n")
lsq12_Eighth.write("echo \"The job ended at $(date).\"")
# Close the average file.
lsq12_Eighth.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# First non-linear (most blurred) ANIMAL registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Open a file to write to; 'a' for append.
nl_First = open("nl_First.sh",'a')
# Add header.
nl_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
# Blur the average and average mask with different kernels. Observe that these blurs (1.4mm), relative to those at the 12-parameter stage, are much larger.
nl_First.write(MNC_Blur + "1.4 " + lsq12_Avg + " " + lsq12_Avg_1400 + "\n")
nl_First.write(MNC_Blur + "1.4 " + LM_Avg_Mask + " " + LM_Avg_Mask_1400 + "\n\n")
nl_First.write("echo \"The job ended at $(date).\"")
nl_First.close()

# Create .sh files for the first round of subset non-linear commands (nl_1).
for Element in list(range(Subset_Specimen_List_Length)):
	# Open a file to write to; 'a' for append.
	nl_Second = open("nl_Second_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Subset_SpecID in Subset_Specimen_IDs[(Subset_Specimen_Group*Element):(Subset_Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Second.write(MNC_Blur + "1.4 " + lsq12_MNC_path + Subset_SpecID + "_lsq12.mnc " + nl_Blurred_path + Subset_SpecID + "_1400\n")
		# Registration string.
		nl_Second.write(nl_1_Register_1400_Blur_Begin + nl_Blurred_path + Subset_SpecID + "_1400_blur.mnc " + lsq12_Avg_1400_Blur + " " + nl_XFM_path + Subset_SpecID + "_nl_1.xfm -model_mask " + LM_Avg_Mask_1400_Blur + " " + nl_1_Register_1400_Blur_End + "\n")
		# Concatenate .xfm files.
		nl_Second.write("xfmconcat -clobber " + lsq6_XFM_path + Subset_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Subset_SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + Subset_SpecID + "_nl_1.xfm " + nl_XFM_path + Subset_SpecID + "_origtonl_1.xfm\n")
		# Resample source image into the first on-linear space with concatenated .xfm.
		nl_Second.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Subset_SpecID + "_origtonl_1.xfm " + Source_MNC_path + Subset_SpecID + ".mnc "+ nl_MNC_path + Subset_SpecID + "_nl_1.mnc\n\n")
	nl_Second.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Second.close()

# Begin a counter.
nl_1_Counter=-1
# Create .sh files for the first round of remainder non-linear commands (nl_1).
# The range should be (#subset specimens, #total specimens).
for Element in list(range(Subset_Specimen_List_Length,Specimen_List_Length)):
	nl_1_Counter += 1
	# Open a file to write to; 'a' for append.
	nl_Third = open("nl_Second_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"Starting run at: $(date).\"\n\n")
	for Remainder_SpecID in Remainder_Specimen_IDs[(Remainder_Specimen_Group*nl_1_Counter):(Remainder_Specimen_Group*(nl_1_Counter+1))]:
		# Blur string.
		nl_Third.write(MNC_Blur + "1.4 " + lsq12_MNC_path + Remainder_SpecID + "_lsq12.mnc " + nl_Blurred_path + Remainder_SpecID + "_1400\n")
		# Registration string.
		nl_Third.write(nl_1_Register_1400_Blur_Begin + nl_Blurred_path + Remainder_SpecID + "_1400_blur.mnc " + lsq12_Avg_1400_Blur + " " + nl_XFM_path + Remainder_SpecID + "_nl_1.xfm -model_mask " + LM_Avg_Mask_1400_Blur + " " + nl_1_Register_1400_Blur_End + "\n")
		# Concatenate .xfm files.
		nl_Third.write("xfmconcat -clobber " + lsq6_XFM_path + Remainder_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_2.xfm " + nl_XFM_path + Remainder_SpecID + "_nl_1.xfm " + nl_XFM_path + Remainder_SpecID + "_origtonl_1.xfm\n")
		# Resample source image into the first on-linear space with concatenated .xfm.
		nl_Third.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Remainder_SpecID + "_origtonl_1.xfm " + Source_MNC_path + Remainder_SpecID + ".mnc "+ nl_MNC_path + Remainder_SpecID + "_nl_1.mnc\n\n")
	nl_Third.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Third.close()

# Average the non-linear files from the first set of deformations.
for SpecID in Specimen_IDs:
	nl_1_MNC_Avg += nl_MNC_path + SpecID + "_nl_1.mnc "
# Open a file to write to; 'a' for append.
nl_Fourth = open("nl_Third.sh",'a')
# Add header.
nl_Fourth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Fourth.write("echo \"All of the first non-linearly deformed files are being averaged.\"\n")
nl_Fourth.write(nl_1_MNC_Avg + nl_1_Avg + "\n\n")
# Blur string for the average and average mask.
nl_Fourth.write("echo \"Blur this first non-linear average, as it will become the target in the next set of the hierarchical non-linear deformations.\"\n")
nl_Fourth.write(MNC_Blur + "1.0 " + nl_1_Avg + " " + nl_1_Avg_1000 + "\n")
nl_Fourth.write(MNC_Blur + "1.0 " + LM_Avg_Mask + " " + LM_Avg_Mask_1000 + "\n\n")
nl_Fourth.write("echo \"The job ended at $(date).\"")
# Close the script.
nl_Fourth.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Second non-linear (second most blurred) ANIMAL registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create .sh files for the second round of non-linear commands (nl_2).
for Element in list(range(Subset_Specimen_List_Length)):
	# Open a file to write to; 'a' for append.
	nl_Fifth = open("nl_Fourth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Fifth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Subset_SpecID in Subset_Specimen_IDs[(Subset_Specimen_Group*Element):(Subset_Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Fifth.write(MNC_Blur + "1.0 " + lsq12_MNC_path + Subset_SpecID + "_lsq12.mnc " + nl_Blurred_path + Subset_SpecID + "_1000\n")
		# Registration string.
		nl_Fifth.write(nl_2_Register_1000_Blur_Begin + nl_Blurred_path + Subset_SpecID + "_1000_blur.mnc " + nl_1_Avg_1000_Blur + " " + nl_XFM_path + Subset_SpecID + "_nl_2.xfm -model_mask " + LM_Avg_Mask_1000_Blur + " " + nl_2_Register_1000_Blur_End + nl_XFM_path + Subset_SpecID + "_nl_1.xfm\n")
		# Concatenate .xfm files.
		nl_Fifth.write("xfmconcat -clobber " + lsq6_XFM_path + Subset_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Subset_SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + Subset_SpecID + "_nl_2.xfm " + nl_XFM_path + Subset_SpecID + "_origtonl_2.xfm\n")
		# Resample source image into the second non-linear space with concatenated .xfm.
		nl_Fifth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Subset_SpecID + "_origtonl_2.xfm " + Source_MNC_path + Subset_SpecID + ".mnc "+ nl_MNC_path + Subset_SpecID + "_nl_2.mnc\n\n")
	nl_Fifth.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Fifth.close()

# Begin a counter.
nl_2_Counter=-1
# Create .sh files for the second round of remainder non-linear commands (nl_2).
# The range should be (#subset specimens, #total specimens).
for Element in list(range(Subset_Specimen_List_Length,Specimen_List_Length)):
	nl_2_Counter += 1
	# Open a file to write to; 'a' for append.
	nl_Sixth = open("nl_Fourth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Sixth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Remainder_SpecID in Remainder_Specimen_IDs[(Remainder_Specimen_Group*nl_2_Counter):(Remainder_Specimen_Group*(nl_2_Counter+1))]:
		# Blur string.
		nl_Sixth.write(MNC_Blur + "1.0 " + lsq12_MNC_path + Remainder_SpecID + "_lsq12.mnc " + nl_Blurred_path + Remainder_SpecID + "_1000\n")
		# Registration string.
		nl_Sixth.write(nl_2_Register_1000_Blur_Begin + nl_Blurred_path + Remainder_SpecID + "_1000_blur.mnc " + nl_1_Avg_1000_Blur + " " + nl_XFM_path + Remainder_SpecID + "_nl_2.xfm -model_mask " + LM_Avg_Mask_1000_Blur + " " + nl_2_Register_1000_Blur_End + nl_XFM_path + Remainder_SpecID + "_nl_1.xfm\n")
		# Concatenate .xfm files.
		nl_Sixth.write("xfmconcat -clobber " + lsq6_XFM_path + Remainder_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_2.xfm " + nl_XFM_path + Remainder_SpecID + "_nl_2.xfm " + nl_XFM_path + Remainder_SpecID + "_origtonl_2.xfm\n")
		# Resample source image into the first on-linear space with concatenated .xfm.
		nl_Sixth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Remainder_SpecID + "_origtonl_2.xfm " + Source_MNC_path + Remainder_SpecID + ".mnc "+ nl_MNC_path + Remainder_SpecID + "_nl_2.mnc\n\n")
	nl_Sixth.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Sixth.close()

# Average the non-linear files from the second set of deformations.
for SpecID in Specimen_IDs:
	nl_2_MNC_Avg += nl_MNC_path + SpecID + "_nl_2.mnc "
# Open a file to write to; 'a' for append.
nl_Seventh = open("nl_Fifth.sh",'a')
# Add header.
nl_Seventh.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Seventh.write("echo \"All of the second non-linearly deformed files are being averaged.\"\n")
nl_Seventh.write(nl_2_MNC_Avg + nl_2_Avg + "\n\n")
# Blur string for the average and average mask.
nl_Seventh.write("echo \"Blur this second non-linear average, as it will become the target in the next set of the hierarchical non-linear deformations.\"\n")
nl_Seventh.write(MNC_Blur + "0.7 " + nl_2_Avg + " " + nl_2_Avg_700 + "\n")
nl_Seventh.write(MNC_Blur + "0.7 " + LM_Avg_Mask + " " + LM_Avg_Mask_700 + "\n\n")
nl_Seventh.write("echo \"The job ended at $(date).\"")
# Close the script.
nl_Seventh.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Third non-linear (third most blurred) ANIMAL registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create .sh files for the third round of non-linear commands (nl_3).
for Element in list(range(Subset_Specimen_List_Length)):
	# Open a file to write to; 'a' for append.
	nl_Eighth = open("nl_Sixth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Eighth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Subset_SpecID in Subset_Specimen_IDs[(Subset_Specimen_Group*Element):(Subset_Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Eighth.write(MNC_Blur + "0.7 " + lsq12_MNC_path + Subset_SpecID + "_lsq12.mnc " + nl_Blurred_path + Subset_SpecID + "_700\n")
		# Registration string.
		nl_Eighth.write(nl_3_Register_700_Blur_Begin + nl_Blurred_path + Subset_SpecID + "_700_blur.mnc " + nl_2_Avg_700_Blur + " " + nl_XFM_path + Subset_SpecID + "_nl_3.xfm -model_mask " + LM_Avg_Mask_700_Blur + " " + nl_3_Register_700_Blur_End + nl_XFM_path + Subset_SpecID + "_nl_2.xfm\n")
		# Concatenate .xfm files.
		nl_Eighth.write("xfmconcat -clobber " + lsq6_XFM_path + Subset_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Subset_SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + Subset_SpecID + "_nl_3.xfm " + nl_XFM_path + Subset_SpecID + "_origtonl_3.xfm\n")
		# Resample source image into third non-linear space with concatenated .xfm.
		nl_Eighth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Subset_SpecID + "_origtonl_3.xfm " + Source_MNC_path + Subset_SpecID + ".mnc "+ nl_MNC_path + Subset_SpecID + "_nl_3.mnc\n\n")
	nl_Eighth.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Eighth.close()

# Begin a counter.
nl_3_Counter=-1
# Create .sh files for the third round of remainder non-linear commands (nl_3).
# The range should be (#subset specimens, #total specimens).
for Element in list(range(Subset_Specimen_List_Length,Specimen_List_Length)):
	nl_3_Counter += 1
	# Open a file to write to; 'a' for append.
	nl_Ninth = open("nl_Sixth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Ninth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Remainder_SpecID in Remainder_Specimen_IDs[(Remainder_Specimen_Group*nl_3_Counter):(Remainder_Specimen_Group*(nl_3_Counter+1))]:
		# Blur string.
		nl_Ninth.write(MNC_Blur + "0.7 " + lsq12_MNC_path + Remainder_SpecID + "_lsq12.mnc " + nl_Blurred_path + Remainder_SpecID + "_700\n")
		# Registration string.
		nl_Ninth.write(nl_3_Register_700_Blur_Begin + nl_Blurred_path + Remainder_SpecID + "_700_blur.mnc " + nl_2_Avg_700_Blur + " " + nl_XFM_path + Remainder_SpecID + "_nl_3.xfm -model_mask " + LM_Avg_Mask_700_Blur + " " + nl_3_Register_700_Blur_End + nl_XFM_path + Remainder_SpecID + "_nl_2.xfm\n")
		# Concatenate .xfm files.
		nl_Ninth.write("xfmconcat -clobber " + lsq6_XFM_path + Remainder_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_2.xfm " + nl_XFM_path + Remainder_SpecID + "_nl_3.xfm " + nl_XFM_path + Remainder_SpecID + "_origtonl_3.xfm\n")
		# Resample source image into the first on-linear space with concatenated .xfm.
		nl_Ninth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Remainder_SpecID + "_origtonl_3.xfm " + Source_MNC_path + Remainder_SpecID + ".mnc "+ nl_MNC_path + Remainder_SpecID + "_nl_3.mnc\n\n")
	nl_Ninth.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Ninth.close()

# Average the non-linear files from the third set of deformations.
for SpecID in Specimen_IDs:
	nl_3_MNC_Avg += nl_MNC_path + SpecID + "_nl_3.mnc "
# Open a file to write to; 'a' for append.
nl_Tenth = open("nl_Seventh.sh",'a')
# Add header.
nl_Tenth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Tenth.write("echo \"All of the third non-linearly deformed files are being averaged.\"\n")
nl_Tenth.write(nl_3_MNC_Avg + nl_3_Avg + "\n\n")
# Blur string for the average and average mask.
nl_Tenth.write("echo \"Blur this third non-linear average, as it will become the target in the next set of the hierarchical non-linear deformations.\"\n")
nl_Tenth.write(MNC_Blur + "0.4 " + nl_3_Avg + " " + nl_3_Avg_400 + "\n")
nl_Tenth.write(MNC_Blur + "0.4 " + LM_Avg_Mask + " " + LM_Avg_Mask_400 + "\n\n")
nl_Tenth.write("echo \"The job ended at $(date).\"")
# Close the script.
nl_Tenth.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Fourth non-linear (fourth most blurred) ANIMAL registration stage.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create .sh files for the fourth round of non-linear commands (nl_4).
for Element in list(range(Subset_Specimen_List_Length)):
	# Open a file to write to; 'a' for append.
	nl_Eleventh = open("nl_Eighth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Eleventh.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Subset_SpecID in Subset_Specimen_IDs[(Subset_Specimen_Group*Element):(Subset_Specimen_Group*(Element+1))]:
		# Blur string.
		nl_Eleventh.write(MNC_Blur + "0.4 " + lsq12_MNC_path + Subset_SpecID + "_lsq12.mnc " + nl_Blurred_path + Subset_SpecID + "_400\n")
		# Registration string.
		nl_Eleventh.write(nl_4_Register_400_Blur_Begin + nl_Blurred_path + Subset_SpecID + "_400_blur.mnc " + nl_3_Avg_400_Blur + " " + nl_XFM_path + Subset_SpecID + "_nl_4.xfm -model_mask " + LM_Avg_Mask_400_Blur + " " + nl_4_Register_400_Blur_End + nl_XFM_path + Subset_SpecID + "_nl_3.xfm\n")
		# Concatenate .xfm files.
		nl_Eleventh.write("xfmconcat -clobber " + lsq6_XFM_path + Subset_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Subset_SpecID + "_lsq12_AVG.xfm " + nl_XFM_path + Subset_SpecID + "_nl_4.xfm " + nl_XFM_path + Subset_SpecID + "_origtonl_4.xfm\n")
		# Resample source image into third non-linear space with concatenated .xfm.
		nl_Eleventh.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Subset_SpecID + "_origtonl_4.xfm " + Source_MNC_path + Subset_SpecID + ".mnc "+ nl_MNC_path + Subset_SpecID + "_nl_4.mnc\n\n")
	nl_Eleventh.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Eleventh.close()

# Begin a counter.
nl_4_Counter=-1
# Create .sh files for the fourth round of remainder non-linear commands (nl_4).
# The range should be (#subset specimens, #total specimens).
for Element in list(range(Subset_Specimen_List_Length,Specimen_List_Length)):
	nl_4_Counter += 1
	# Open a file to write to; 'a' for append.
	nl_Twelfth = open("nl_Eighth_" + str(Element) + ".sh",'a')
	# Add header.
	nl_Twelfth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
	for Remainder_SpecID in Remainder_Specimen_IDs[(Remainder_Specimen_Group*nl_4_Counter):(Remainder_Specimen_Group*(nl_4_Counter+1))]:
		# Blur string.
		nl_Twelfth.write(MNC_Blur + "0.4 " + lsq12_MNC_path + Remainder_SpecID + "_lsq12.mnc " + nl_Blurred_path + Remainder_SpecID + "_400\n")
		# Registration string.
		nl_Twelfth.write(nl_4_Register_400_Blur_Begin + nl_Blurred_path + Remainder_SpecID + "_400_blur.mnc " + nl_3_Avg_400_Blur + " " + nl_XFM_path + Remainder_SpecID + "_nl_4.xfm -model_mask " + LM_Avg_Mask_400_Blur + " " + nl_4_Register_400_Blur_End + nl_XFM_path + Remainder_SpecID + "_nl_3.xfm\n")
		# Concatenate .xfm files.
		nl_Twelfth.write("xfmconcat -clobber " + lsq6_XFM_path + Remainder_SpecID + "_lsq6_2.xfm " + lsq12_XFM_path + Remainder_SpecID + "_to_average_lsq12_2.xfm " + nl_XFM_path + Remainder_SpecID + "_nl_4.xfm " + nl_XFM_path + Remainder_SpecID + "_origtonl_4.xfm\n")
		# Resample source image into the first on-linear space with concatenated .xfm.
		nl_Twelfth.write("mincresample -like " + LM_Avg + " -clobber -transformation " + nl_XFM_path + Remainder_SpecID + "_origtonl_4.xfm " + Source_MNC_path + Remainder_SpecID + ".mnc "+ nl_MNC_path + Remainder_SpecID + "_nl_4.mnc\n\n")
	nl_Twelfth.write("echo \"The job ended at $(date).\"")
	# Close the script.
	nl_Twelfth.close()

# Average the non-linear files from the fourth set of deformations.
for SpecID in Specimen_IDs:
	nl_4_MNC_Avg += nl_MNC_path + SpecID + "_nl_4.mnc "
# Open a file to write to; 'a' for append.
nl_Thirteenth = open("nl_Ninth.sh",'a')
# Add header.
nl_Thirteenth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=15000M\n#SBATCH --time=11:00:00\n\nmodule load minc-toolkit/2016-11\n\ncd " + Scripts_path + "\n\necho \"The job started at $(date).\"\n\n")
nl_Thirteenth.write("echo \"All of the fourth non-linearly deformed files are being averaged.\"\n")
nl_Thirteenth.write(nl_4_MNC_Avg + nl_4_Avg + "\n\n")
nl_Thirteenth.write("echo \"The job ended at $(date).\"")
# Close the script.
nl_Thirteenth.close()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create master job submission scripts for all stages. These scripts will automatically submit all .sh scripts to the queue and will be chained together. In other words, only the first script, Job_Submission_First.sh, needs to be submitted.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Job_Submission_First (i.e., 6-parameter blurs, registrations, concatenations, resamplings, and the average).
Job_Submission_First = open("Job_Submission_First.sh",'a')
Job_Submission_First.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_First.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_First.write("cd " + Scripts_path + "\n\n")
Job_Submission_First.write("sleep 10\n\n")
Job_Submission_First.write("lsq6_First=$(sbatch lsq6_First.sh)\n\n")
Job_Submission_First.write("until [[ $(squeue -t CD -u $USER --noheader -j ${lsq6_First##* } | wc -l) -eq 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_First.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq6_Second_$NUM.sh\"\nLSQ6=\"sbatch $NAME\"\n$LSQ6\necho $LSQ6\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_First.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_First.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_First.write("# Submit 6-parameter average script.\nlsq6_Third=$(sbatch lsq6_Third.sh)\n\n")
Job_Submission_First.write("#----------------------------------------------------- Submit next job submission script after average finishes and remove current submission script from the queue.\n\n")
Job_Submission_First.write("sbatch --dependency=afterok:${lsq6_Third##* } Job_Submission_Second.sh\n\n")
Job_Submission_First.write("echo \"The job ended at $(date).\"\n")
Job_Submission_First.write("scancel -u $USER --jobname=Job_Submission_First.sh")
Job_Submission_First.close()
# Job_Submission_Second (i.e., 12-parameter blurs).
Job_Submission_Second = open("Job_Submission_Second.sh",'a')
Job_Submission_Second.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Second.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Second.write("cd " + Scripts_path + "\n\n")
Job_Submission_Second.write("sleep 10\n\n")
Job_Submission_Second.write("lsq12_First=$(sbatch lsq12_First.sh)\n\n")
Job_Submission_Second.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 1 " + str(Specimen_List_Length) + ")\n\n")
Job_Submission_Second.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Second_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Second.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Second.write("# Create while loop to idle submission script before the registrations.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Second.write("#----------------------------------------------------- Submit 12-parameter registration job submission script and remove current submission script from the queue.\n\n")
Job_Submission_Second.write("Job_Submission_Third=$(sbatch Job_Submission_Third.sh)\n\n")
Job_Submission_Second.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Second.write("scancel -u $USER --jobname=Job_Submission_Second.sh")
Job_Submission_Second.close()
# Job_Submission_Third (i.e., 12-parameter registrations between the subset of specimens).
Job_Submission_Third = open("Job_Submission_Third.sh",'a')
Job_Submission_Third.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Third.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Third.write("cd " + Scripts_path + "\n\n")
Job_Submission_Third.write("sleep 10\n\n")
Job_Submission_Third.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Subset_Specimen_Upper) + ")\n\n")
Job_Submission_Third.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Third_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Third.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Third.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Third.write("#----------------------------------------------------- Submit xfm average, concatenating, and resampling job submission script and remove current submission script from the queue.\n\n")
Job_Submission_Third.write("Job_Submission_Fourth=$(sbatch Job_Submission_Fourth.sh)\n\n")
Job_Submission_Third.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Third.write("scancel -u $USER --jobname=Job_Submission_Third.sh")
Job_Submission_Third.close()
# Job_Submission_Fourth (i.e., 12-parameter concatenations, resamplings, and averaging the subset).
Job_Submission_Fourth = open("Job_Submission_Fourth.sh",'a')
Job_Submission_Fourth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Fourth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Fourth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Fourth.write("sleep 10\n\n")
Job_Submission_Fourth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Subset_Specimen_List_Length-1) + ")\n\n")
Job_Submission_Fourth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Fourth_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Fourth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Fourth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Fourth.write("#----------------------------------------------------- Submit lsq12 subset average job submission script and the remainder specimen 12-parameter registration dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Fourth.write("lsq12_Fifth=$(sbatch lsq12_Fifth.sh)\n\n")
Job_Submission_Fourth.write("sbatch --dependency=afterok:${lsq12_Fifth##* } Job_Submission_Fifth.sh\n\n")
Job_Submission_Fourth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Fourth.write("scancel -u $USER --jobname=Job_Submission_Fourth.sh")
Job_Submission_Fourth.close()
# Job_Submission_Fifth (i.e., 12-parameter registrations between the subset average and all remainder specimens).
Job_Submission_Fifth = open("Job_Submission_Fifth.sh",'a')
Job_Submission_Fifth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Fifth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Fifth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Fifth.write("sleep 10\n\n")
Job_Submission_Fifth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Remainder_Specimen_Upper) + ")\n\n")
Job_Submission_Fifth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Sixth_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Fifth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Fifth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Fifth.write("#----------------------------------------------------- Submit xfm average, concatenating, and resampling job submission script and remove current submission script from the queue.\n\n")
Job_Submission_Fifth.write("Job_Submission_Sixth=$(sbatch Job_Submission_Sixth.sh)\n\n")
Job_Submission_Fifth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Fifth.write("scancel -u $USER --jobname=Job_Submission_Fifth.sh")
Job_Submission_Fifth.close()
# Job_Submission_Sixth (i.e., 12-parameter concatenations, resamplings, and averaging the remainder specimens in conjunction with the previous subset for a global 12-parameter average).
Job_Submission_Sixth = open("Job_Submission_Sixth.sh",'a')
Job_Submission_Sixth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Sixth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Sixth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Sixth.write("sleep 10\n\n")
Job_Submission_Sixth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Remainder_Specimen_Upper) + ")\n\n")
Job_Submission_Sixth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"lsq12_Seventh_$NUM.sh\"\nLSQ12=\"sbatch $NAME\"\n$LSQ12\necho $LSQ12\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Sixth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Sixth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Sixth.write("#----------------------------------------------------- Submit lsq12 global average job submission script and the first non-linear registration dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Sixth.write("lsq12_Eighth=$(sbatch lsq12_Eighth.sh)\n\n")
Job_Submission_Sixth.write("sbatch --dependency=afterok:${lsq12_Eighth##* } Job_Submission_Seventh.sh\n\n")
Job_Submission_Sixth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Sixth.write("scancel -u $USER --jobname=Job_Submission_Sixth.sh")
Job_Submission_Sixth.close()
# Job_Submission_Seventh (i.e., NL_1 and the first hierarchical non-linear registration).
Job_Submission_Seventh = open("Job_Submission_Seventh.sh",'a')
Job_Submission_Seventh.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Seventh.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Seventh.write("cd " + Scripts_path + "\n\n")
Job_Submission_Seventh.write("sleep 10\n\n")
Job_Submission_Seventh.write("nl_First=$(sbatch nl_First.sh)\n\n")
Job_Submission_Seventh.write("until [[ $(squeue -t CD -u $USER --noheader -j ${nl_First##* } | wc -l) -eq 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Seventh.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Seventh.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Second_$NUM.sh\"\nNL1=\"sbatch $NAME\"\n$NL1\necho $NL1\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Seventh.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Seventh.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Seventh.write("#----------------------------------------------------- Submit NL_1 average job submission script and the second non-linear (NL_2) dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Seventh.write("nl_Third=$(sbatch nl_Third.sh)\n\n")
Job_Submission_Seventh.write("sbatch --dependency=afterok:${nl_Third##* } Job_Submission_Eighth.sh\n\n")
Job_Submission_Seventh.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Seventh.write("scancel -u $USER --jobname=Job_Submission_Seventh.sh")
Job_Submission_Seventh.close()
# Job_Submission_Eighth (i.e., NL_2 and the second hierarchical non-linear registration).
Job_Submission_Eighth = open("Job_Submission_Eighth.sh",'a')
Job_Submission_Eighth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Eighth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Eighth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Eighth.write("sleep 10\n\n")
Job_Submission_Eighth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Eighth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Fourth_$NUM.sh\"\nNL2=\"sbatch $NAME\"\n$NL2\necho $NL2\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Eighth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Eighth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Eighth.write("#----------------------------------------------------- Submit NL_2 average job submission script and the third non-linear (NL_3) dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Eighth.write("nl_Fifth=$(sbatch nl_Fifth.sh)\n\n")
Job_Submission_Eighth.write("sbatch --dependency=afterok:${nl_Fifth##* } Job_Submission_Ninth.sh\n\n")
Job_Submission_Eighth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Eighth.write("scancel -u $USER --jobname=Job_Submission_Eighth.sh")
Job_Submission_Eighth.close()
# Job_Submission_Ninth (i.e., NL_3 and the third hierarchical non-linear registration).
Job_Submission_Ninth = open("Job_Submission_Ninth.sh",'a')
Job_Submission_Ninth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Ninth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Ninth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Ninth.write("sleep 10\n\n")
Job_Submission_Ninth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Ninth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Sixth_$NUM.sh\"\nNL3=\"sbatch $NAME\"\n$NL3\necho $NL3\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Ninth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Ninth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Ninth.write("#----------------------------------------------------- Submit NL_3 average job submission script and the fourth non-linear (NL_4) dependency, then remove current submission script from the queue.\n\n")
Job_Submission_Ninth.write("nl_Seventh=$(sbatch nl_Seventh.sh)\n\n")
Job_Submission_Ninth.write("sbatch --dependency=afterok:${nl_Seventh##* } Job_Submission_Tenth.sh\n\n")
Job_Submission_Ninth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Ninth.write("scancel -u $USER --jobname=Job_Submission_Ninth.sh")
Job_Submission_Ninth.close()
# Job_Submission_Tenth (i.e., NL_4 and the fourth hierarchical non-linear registration).
Job_Submission_Tenth = open("Job_Submission_Tenth.sh",'a')
Job_Submission_Tenth.write("#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --mem=2000M\n#SBATCH --time=05-00:00:00\n#SBATCH --job-name=Job_Submission_Tenth.sh\n\necho \"The job started at $(date).\"\n\n")
Job_Submission_Tenth.write("cd " + Scripts_path + "\n\n")
Job_Submission_Tenth.write("sleep 10\n\n")
Job_Submission_Tenth.write("# Generate a sequence of numbers.\nNUMBERS=$(seq 0 " + str(Specimen_List_Length-1) + ")\n\n")
Job_Submission_Tenth.write("# For loop to automatically submit your jobs.\nfor NUM in $NUMBERS; do\nNAME=\"nl_Eighth_$NUM.sh\"\nNL4=\"sbatch $NAME\"\n$NL4\necho $NL4\n# Sleep script in 3 second intervals.\nsleep 3\ndone\n\n")
Job_Submission_Tenth.write("# Sleep script for 5 seconds before while loop.\nsleep 5\n\n")
Job_Submission_Tenth.write("# Create while loop to idle submission script before the averaging.\nwhile [[ $(squeue -t R -u $USER --noheader | wc -l) -gt 1 ]]; do\nsleep 5\ndone\n\n")
Job_Submission_Tenth.write("#----------------------------------------------------- Submit final NL_4 average script.\n\n")
Job_Submission_Tenth.write("nl_Ninth=$(sbatch nl_Ninth.sh)\n\n")
Job_Submission_Tenth.write("echo \"The job ended at $(date).\"\n")
Job_Submission_Tenth.close()
