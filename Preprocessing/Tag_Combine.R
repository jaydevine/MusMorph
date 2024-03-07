# This is an R script that will accept two input .tag files (with >=4  homologous init. markers) and combine them into a two volume tag file that will be converted into a rigid transformation matrix. 

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# You only need to edit the variables within these dashed lines.

# Define the path to thespecimen list file.
FILENAME="/path/to/<PROJECT>/Source/spec_list.txt"
# Define the path to the .tag files.
Source_Tag_path="/path/to/<PROJECT>/Source/Tag"
# Define the name of your reference specimen or atlas, excluding the file extension. 
Atlas=""
# Define your .txt file of specimen names, say spec_list.txt.
All_Specimens=read.table(FILENAME,stringsAsFactors=FALSE)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Define tag combine function. 
Combine_Tag=function(Source_Tag_path,Atlas,SpecID){
  Atlas_LMs=read.table(paste(Source_Tag_path,paste(Atlas,".tag",sep=""),sep="/"), sep=c(" ",";"), skip=4,header=FALSE,stringsAsFactors=FALSE)[,2:4]
  Spec_LMs=read.table(paste(Source_Tag_path,paste(SpecID,".tag",sep=""),sep="/"), sep=c(" ",";"), skip=4,header=FALSE,stringsAsFactors=FALSE)[,2:4]
  N_Atlas_LMs=nrow(Atlas_LMs)
  #Create Output File and add Header
  FileName=paste("Tag_",Atlas,"_to_",SpecID,".tag",sep="")
  cat("MNI Tag Point File\n",file=FileName,append=FALSE)
  cat("Volumes = 2;\n",file=FileName,append=TRUE)
  cat(paste("%VIO_Volume: ",Atlas,".mnc\n",sep=""),file=FileName,append=TRUE)
  cat(paste("%VIO_Volume: ",SpecID,".mnc\n",sep=""),file=FileName,append=TRUE)
  cat("\n",file=FileName,append=TRUE)
  cat("Points = \n",file=FileName,append=TRUE)
  
  #Because we must include numbers and characters in each line, we will cat() each line instead of making a matrix first
  for (i in 1:N_Atlas_LMs) {
    cat(paste(Atlas_LMs[i,1],Atlas_LMs[i,2],Atlas_LMs[i,3],Spec_LMs[i,1],Spec_LMs[i,2],Spec_LMs[i,3],"\n",sep=" "),file=FileName,append=TRUE)
  }
}

setwd(Source_Tag_path)
# Run the tag combine function and output the files to Source_MNC_path. 
for(j in 1:nrow(All_Specimens)){
  Combine_Tag(Source_Tag_path,Atlas,All_Specimens[j,1])
}
