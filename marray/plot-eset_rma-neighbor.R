#!/usr/bin/Rscript
exp_name <- c(commandArgs(trailingOnly=TRUE))
if( length(exp_name) != 1 ) {
  cat("No dataset name\n")
  cat("Usage: Rscript affy-eset_rma-hist.R <dataset_name>\n")
  quit()
}

filename_opposite <- paste(exp_name,'eset_rma','opposite',sep='.')
filename_neighbor <- paste(exp_name,'eset_rma','neighbor',sep='.')
filename_spearman_png <- paste(exp_name,'eset_rma','spearman','png',sep='.')
filename_euclidian_png <- paste(exp_name,'eset_rma','euclidian','png',sep='.')

opposite <- read.table(filename_opposite,header=F)
neighbor <- read.table(filename_neighbor,header=F)

png(filename=filename_spearman_png,width=800,height=600)
hist(neighbor[,12], density=0, breaks=100, col='red', 
      main=paste(exp_name,'Spearman'), xlab='Spearman Correlation Coefficient')
hist(opposite[,12], density=0, breaks=100, col='blue', add=T)
legend('topleft',c('neighbor','opposite'),lty=1,lwd=2,col=c('red','blue'))
dev.off()

png(filename=filename_euclidian_png,width=800,height=600)
hist(log(neighbor[,14])/log(10), density=0, breaks=100, col='red', 
      main=paste(exp_name,'Euclidian'), xlab='Euclidian distance (log10)')
hist(log(opposite[,14])/log(10), density=0, breaks=100, col='blue', add=T)
legend('topright',c('neighbor','opposite'),lty=1,lwd=2,col=c('red','blue'))
dev.off()
