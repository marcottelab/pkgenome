#!/usr/bin/Rscript

dataset_name <- c(commandArgs(trailingOnly=TRUE))
if( length(dataset_name) != 1 ) {
  cat("No dataset name\n")
  cat("Usage: Rscript affy-RMA-plot.R <dataset_name>\n");
  quit()
}

library(affy)

load( paste(dataset_name,'.affybatch_raw',sep='') )
load( paste(dataset_name,'.affybatch_normalized',sep='') )
load( paste(dataset_name,'.eset_rma',sep='') )

## Boxplot
png(filename=paste("plot/",dataset_name,".box_raw.png",sep=''),
      width=1024,height=640);
par(mar=c(10,4,4,2))
boxplot( as.data.frame(log2(intensity(affybatch_raw))), las=2, mex=0.1,
          main=paste(dataset_name,'(raw)',sep=''),
          ylab="log2 intensity")
dev.off();

png(filename=paste("plot/",dataset_name,".box_rma.png", sep=''),
      width=1024,height=640);
par(mar=c(10,4,4,2))
boxplot( as.data.frame(exprs(eset_rma)), las=2, mex=0.1,
      main=paste(dataset_name,"(normalized - RMA)") )
dev.off();

## RMA, log2 intensity
rma_intensity <- as.data.frame(eset_rma);
rma_dist <- dist( as.matrix(rma_intensity) )
rma_clust <- hclust( rma_dist, method="average")
png(filename=paste("plot/",dataset_name,".rma_log_clust.png",sep=''),
        width=1024,height=640);
plot(rma_clust, main=paste(dataset_name,":hclust_average(rma,log2)",sep=''))
dev.off();

## RMA, log2 Rank
rma_rank <- matrix(data=NA, nrow=nrow(eset_rma), ncol=ncol(eset_rma) );
nsample <- ncol(eset_rma)
for(i in 1:nsample) {
  rma_rank[,i] <- rank(exprs(eset_rma[,i]) );
}
colnames(rma_rank) <- sampleNames(eset_rma)
rma_rank_dist <- dist( t(rma_rank) )
rma_rank_clust <- hclust(rma_rank_dist, method="average")
png(filename=paste("plot/",dataset_name,'.rma_rank_clust.png',sep=''), 
      width=1024, height=640);
plot(rma_rank_clust,
      main=paste(dataset_name,":hclust_average(rma,log2_rank)",sep=''))
dev.off()
