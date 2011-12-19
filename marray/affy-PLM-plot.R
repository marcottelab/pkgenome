#!/usr/bin/Rscript

dataset_name <- c(commandArgs(trailingOnly=TRUE))
if( length(dataset_name) != 1 ) {
  cat("No dataset name\n")
  cat("Usage: Rscript affy-PLM-plot.R <dataset_name>\n");
  quit()
}

library(affy)
library(affyPLM)

load( paste(dataset_name,'.affybatch_raw',sep='') )

affybatch_raw_PLM <- fitPLM(affybatch_raw)

sample_names <- sampleNames(affybatch_raw)
for(i in 1:length(sample_names)) {
  filename_img <- paste("plot/",sample_names[i],".PLM_resids.png", sep="")
  png(filename=filename_img, width=1024, height=1024);
  image( affybatch_raw_PLM, which=i, type="resids", add.legend=TRUE )
  dev.off()
}

png(filename=paste('plot/',dataset_name,'.RLE.png',sep=''),
              width=1024,height=800)
par(mar=c(10,4,4,2))
RLE(affybatch_raw_PLM, fin=c(1024, 600), las=2, mex=0.1,
    main=paste("Relative Log Expression(RLE) for ",dataset_name, sep=''))
dev.off()
