# This is an R script that will accept two input .tag files (with >=4  init. markers) and combine them into a two volume tag file that will be converted into a rigid transformation matrix. 

# Define function. 
combo.tag=function(XFM.dir,BaseSpec,SpecName){
  Base.LMs=read.table(paste(Tag.dir,paste(BaseSpec,".tag",sep=""),sep="/"), sep=c(" ",";"), skip=4,header=FALSE,stringsAsFactors=FALSE)[,2:4]
  Spec.LMs=read.table(paste(Tag.dir,paste(SpecName,".tag",sep=""),sep="/"), sep=c(" ",";"), skip=4,header=FALSE,stringsAsFactors=FALSE)[,2:4]
  n.Base.LM=nrow(Base.LMs)
  #Create Output File and add Header
  FileName=paste("Tag_",BaseSpec,"_to_",SpecName,".tag",sep="")
  cat("MNI Tag Point File\n",file=FileName,append=FALSE)
  cat("Volumes = 2;\n",file=FileName,append=TRUE)
  cat(paste("%VIO_Volume: ",BaseSpec,".mnc\n",sep=""),file=FileName,append=TRUE)
  cat(paste("%VIO_Volume: ",SpecName,".mnc\n",sep=""),file=FileName,append=TRUE)
  cat("\n",file=FileName,append=TRUE)
  cat("Points = \n",file=FileName,append=TRUE)
  
  #Because we must include numbers and characters in each line, we will cat() each line instead of making a matrix first
  for (i in 1:n.Base.LM) {
    cat(paste(Base.LMs[i,1],Base.LMs[i,2],Base.LMs[i,3],Spec.LMs[i,1],Spec.LMs[i,2],Spec.LMs[i,3],"\n",sep=" "),file=FileName,append=TRUE)
  }
}

# Define the directory with the specimen list file (below) and where the combined .tag files will end up. 
Source.dir="/path/to/Source/MNC"
# Define the path to the .tag files.
Tag.dir="/path/to/Source/Tag"
# Define your reference specimen or atlas. 
BaseSpec=""
# Define your .txt file of specimen names, say spec_list.txt.
Spec.List=read.table(paste(Source.dir,"spec_list.txt",sep="/"),stringsAsFactors=FALSE)
setwd(Tag.dir)
# Run the tag combine function and output the files to Source.dir. 
for(j in 1:nrow(Spec.List)){
  combo.tag(Source.dir,BaseSpec,Spec.List[j,1])
}
