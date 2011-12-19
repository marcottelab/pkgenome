#!/usr/bin/Rscript

dataset_name <- c(commandArgs(trailingOnly=TRUE))
if( length(dataset_name) != 1 ) {
  cat("No dataset name\n")
  cat("Usage: Rscript affy-MAS5-plot.R <dataset_name>\n");
  quit()
}

library(affy)
library(affyPLM)

load( paste(dataset_name,'.eset_mas5',sep='') )

png(filename=paste("plot/",dataset_name,".box_mas5.png", sep=''),
      width=1024,height=640);
boxplot( as.data.frame(exprs(eset_rma)), 
      main=paste(dataset_name,"(normalized - MAS5)") )
dev.off();

## MAS5, Raw intensity
mas5_intensity <- as.data.frame(eset_mas5);
mas5_dist <- dist( as.matrix(mas5_intensity) )
mas5_clust <- hclust( mas5_dist, method="average")
png(filename=paste("plot/",dataset_name,".mas5_clust.png",sep=''),
      width=1024,height=640);
plot(mas5_clust, 
    main=paste(dataset_name,":hclust_average(mas5,raw)",sep=''))
dev.off();

## MAS5, log2 intensity
mas5_intensity <- as.data.frame(eset_mas5);
mas5_dist <- dist( log2(as.matrix(mas5_intensity)) )
mas5_clust <- hclust( mas5_dist, method="average")
png(filename=paste("plot/",dataset_name,".mas5_clust_log.png",sep=''),
      width=1024,height=640);
plot(mas5_clust, main=paste(dataset_name,":hclust_average(mas5,log2)",sep=''))
dev.off();

## MAS5, log2 rank
mas5_rank <- matrix(data=NA, nrow=nrow(eset_mas5), ncol=ncol(eset_mas5) );
nsample <- ncol(eset_mas5)
for(i in 1:nsample) {
  mas5_rank[,i] <- rank( log2(exprs(eset_mas5[,i])) );
}
colnames(mas5_rank) <- sampleNames(eset_mas5)
mas5_rank_dist <- dist( t(mas5_rank) )
mas5_rank_clust <- hclust(mas5_rank_dist, method="average")

png(filename=paste("plot/",dataset_name,".mas5_rank_clust.png",sep=''), 
      width=1024, height=640);
plot(mas5_rank_clust, 
  main=paste(dataset_name,":hclust_average(mas5,log2_rank)",sep=''))
dev.off()
