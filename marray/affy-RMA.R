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

save(affybatch_raw, file=paste(dataset_name,'.affybatch_raw', sep=''))
write.table(intensity(affybatch_raw), 
            file=paste(dataset_name,'.raw.txt', sep=''))

affybatch_corrected <- bg.correct(affybatch_raw, method='rma')
save(affybatch_corrected,
            file=paste(dataset_name,'.affybatch_corrected', sep=''))
write.table(intensity(affybatch_corrected), 
            file=paste(dataset_name,'.corrected.txt', sep=''))

affybatch_normalized <- normalize(affybatch_corrected, method='quantiles')
save(affybatch_normalized,
            file=paste(dataset_name,'.affybatch_normalized',sep=''))
write.table(intensity(affybatch_normalized), 
            file=paste(dataset_name,'.norm.txt', sep=''))

eset_rma <- rma(affybatch_raw)
save(eset_rma, file=paste(dataset_name,'.eset_rma',sep=''))
write.exprs(eset_rma, 
            file=paste(dataset_name,'.eset_rma.txt',sep=''))
