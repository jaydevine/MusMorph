# This is an R script that will accept two input .tag files (with >=4  homologous init. markers) and combine them into a two volume tag file that will be converted into a rigid transformation matrix.

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# You only need to uncomment and edit the variables below if you don't use raw input.

# Define the path to the specimen list file (e.g., /path/to/<PROJECT>/Source/spec_list.txt)
# FILENAME="/path/to/<PROJECT>/Source/spec_list.txt"
# Define the path to the .tag files.
# TAG_PATH="/path/to/<PROJECT>/Source/Tag"
# Define the basename of your reference specimen or atlas, excluding the file extension (e.g., Calgary_Adult_Skull_Atlas)
# ATLAS=""

cat("Enter the path to the directory containing the .tag files (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/Tag/): ")
TAG_PATH = readLines(file("stdin"), n=1)

cat("Enter the suffix of the .tag files (e.g., .tag): ")
TAG_SUFFIX = readLines(file("stdin"), n=1)

cat("Enter the path to the file containing the list of specimen names (e.g., /mnt/Storage1/Hallgrimsson/Users/Jay/Workshop/Source/spec_list.txt): ")
FILENAME = readLines(file("stdin"), n=1)

cat("Enter the basename of your reference specimen or atlas, excluding the file extension (e.g., Calgary_Adult_Skull_Atlas): ")
ATLAS = readLines(file("stdin"), n=1)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Read file containing list of specimen names
All_Specimens=read.table(FILENAME,stringsAsFactors=FALSE) 

# Define tag combine function. 
Combine_Tag=function(TAG_PATH,ATLAS,SpecID){
  ATLAS_LMs=read.table(paste(TAG_PATH,paste0(ATLAS,TAG_SUFFIX), sep=""), sep=c(" ",";"), skip=4,header=FALSE,stringsAsFactors=FALSE)[,2:4]
  Spec_LMs=read.table(paste(TAG_PATH,paste0(SpecID,TAG_SUFFIX), sep=""), sep=c(" ",";"), skip=4,header=FALSE,stringsAsFactors=FALSE)[,2:4]
  N_ATLAS_LMs=nrow(ATLAS_LMs)
  #Create Output File and add Header
  FileName=paste("Tag_",ATLAS,"_to_",SpecID,".tag",sep="")
  cat("MNI Tag Point File\n",file=FileName,append=FALSE)
  cat("Volumes = 2;\n",file=FileName,append=TRUE)
  cat(paste("%VIO_Volume: ",ATLAS,".mnc\n",sep=""),file=FileName,append=TRUE)
  cat(paste("%VIO_Volume: ",SpecID,".mnc\n",sep=""),file=FileName,append=TRUE)
  cat("\n",file=FileName,append=TRUE)
  cat("Points = \n",file=FileName,append=TRUE)
  
  #Because we must include numbers and characters in each line, we will cat() each line instead of making a matrix first
  for (i in 1:N_ATLAS_LMs) {
    cat(paste(ATLAS_LMs[i,1],ATLAS_LMs[i,2],ATLAS_LMs[i,3],Spec_LMs[i,1],Spec_LMs[i,2],Spec_LMs[i,3],"\n",sep=" "),file=FileName,append=TRUE)
  }
}

setwd(TAG_PATH)
# Run the tag combine function and output the files to Source_MNC_path. 
for(j in 1:nrow(All_Specimens)){
  Combine_Tag(TAG_PATH,ATLAS,All_Specimens[j,1])
}

