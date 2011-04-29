#!/usr/bin/Rscript
dirname_LLS <- c(commandArgs(trailingOnly=TRUE))
if( length(dirname_LLS) != 1 ) {
  cat("Usage: Rscript predict-LLS.R <LLS directory with *.train.* and *.LLS.* files>\n")
  quit()
}

for( filename_train in list.files(path=dirname_LLS,pattern=".train.[0-9]+",full.names=TRUE) ) {
  cat(paste("Read ",filename_train," ... ",sep=''),file=stderr())
  filename_test = sub('.train.','.test.',filename_train)
  filename_LLS = sub('.train.','.LLS.',filename_train)
  filename_LLS_png = paste(sub('.train.','.LLS.',filename_train),'png',sep='.')
  filename_train_LLS = sub('.train.','.train_LLS.',filename_train)
  filename_test_LLS = sub('.train.','.test_LLS.',filename_train)
  cat("Done\n",file=stderr())

  train <- read.table(filename_train, header=F)
  test <- read.table(filename_test, header=F)
  LLS <- read.table(filename_LLS, header=F)
  colnames(LLS) <- c('Score','LinkageScore')
  colnames(train) <- c('Gene1','Gene2','Score','LinkageScore')
  colnames(test) <- c('Gene1','Gene2','Score','LinkageScore')

  cat("Loess training ... ", file=stderr())
  loess_train <- loess(LinkageScore ~ Score, LLS, span=0.25,
                        control=loess.control(surface="direct"))
  cat("Done\n",file=stderr())

  cat("Loess prediction ... ",file=stderr())
  LLS_train <- predict(loess_train, train$Score)
  LLS_test <- predict(loess_train, test$Score)
  cat("Done\n",file=stderr())

  plot_title = sub('.train.','.',filename_train)
  png(filename_LLS_png, width=600, height=600)
  plot(LLS$Score, LLS$LinkageScore, 
      xlab="Score", ylab="LLS", cex=0.6)
      #main=paste(plot_title,'(bin_size=250, step_size=50)'), cex=0.6)
  points(train$Score, LLS_train, col='blue', cex=0.6, pch=22)
  points(test$Score, LLS_test, col='red', cex=0.2, pch=22)
  legend("bottomright", legend=c('train set','test set'),lty=1, lwd=3, col=c('blue','red'))
  dev.off()

  write.table(cbind(train,LLS_train), file=filename_train_LLS)
  write.table(cbind(test,LLS_test), file=filename_test_LLS)
}
