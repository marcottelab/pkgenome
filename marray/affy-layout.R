#!/usr/bin/Rscript
dataset_name <- c(commandArgs(trailingOnly=TRUE))
if( length(dataset_name) != 1 ) {
  cat("No dataset name\n")
  cat("Usage: Rscript affy-RMA.R <dataset_name>\n")
  quit()
}

library(affy)

exp_table <- read.table(file="EXP",header=T,stringsAsFactors=FALSE,sep="\t")
files_vector <- as.vector(exp_table$Filename,mode='character')
samples_vector <- as.vector(exp_table$Sample,mode='character')
affybatch_raw <- ReadAffy(filenames=files_vector,sampleNames=samples_vector)

pm_idx <- indexProbes(affybatch_raw, which="pm")
for( probeset in pm_idx ) {
  for( probe_idx in probeset ) {
    xy <- indices2xy(probe_idx,abatch=affybatch_raw)
    write( paste(probe_idx,xy[1],xy[2],sep=" "),
          file=paste(dataset_name,'.layout.txt',sep=''), append=TRUE)
  }
}
