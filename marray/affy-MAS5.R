#!/usr/bin/Rscript
dataset_name <- c(commandArgs(trailingOnly=TRUE))
if( length(dataset_name) != 1 ) {
  cat("No dataset name\n")
  cat("Usage: Rscript affy-MAS5.R <dataset_name>\n")
  quit()
}

library(affy)

exp_table <- read.table(file="EXP",header=T,stringsAsFactors=FALSE)

files_vector <- as.vector(exp_table$Filename,mode='character')
samples_vector <- as.vector(exp_table$Sample,mode='character')
affybatch_raw <- ReadAffy(filenames=files_vector,sampleNames=samples_vector)

save(affybatch_raw, file=paste('./',dataset_name,'.affybatch_raw', sep=''))
write.table(intensity(affybatch_raw), 
            file=paste('./',dataset_name,'.raw.txt', sep=''))

eset_mas5 <- mas5(affybatch_raw)
save(eset_mas5, file=paste('./',dataset_name,'.eset_mas5',sep=''))
write.exprs(eset_mas5, 
            file=paste('./',dataset_name,'.eset_mas5.txt',sep=''))

calls_mas5 <- mas5calls(affybatch_raw)
write.exprs(calls_mas5, 
            file=paste('./',dataset_name,'.calls_mas5.txt',sep=''))
