#init db
library(mongolite)
library(ggplot2)
pept_all <- mongo(collection="dip_complexr100", db="bioregulation", url="mongodb://localhost:27017/");
#find index of dipeptide
pepts <- pept_all$find()$c_dip_stat[1:400]
pept <- pept_all$find()$c_dip_stat[which(pept_all$find()$dipeptide == "EL")]

plot(pept[[1]]$cytoplasm, type = 'h')
plot(pept[[1]]$nucleus, pept[[1]]$mean_c, type='h')

res <- cor.test(pepts[[222]]$nucleus[pepts[[222]]$mean_c>0], pepts[[222]]$mean_c[pepts[[222]]$mean_c>0], method = 'spearman')
resname <- pept_all$find()$dipeptide[[2]]

  
make_corr_list <- function(loc, cor_level){
  out <- data.frame()
  for (i in 1:400){
    # res <- cor.test(pepts[[i]][[loc]], pepts[[i]]$mean_c, method = 'spearman')
    res <- cor.test(pepts[[i]][[loc]][pepts[[i]]$mean_c>0], pepts[[i]]$mean_c[pepts[[i]]$mean_c>0], method = 'spearman')
    if (res$estimate >= cor_level || res$estimate <= - cor_level) {
      out <- rbind(out, data.frame(i, pept_all$find()$dipeptide[[i]], res$estimate))
      print(pept_all$find()$dipeptide[[i]])
      print(res$estimate)
      print('------------------') 
    }
  }
  return (out)
}
# 1"nucleus" 2"cytoplasm" 3 "membrane"  4 "extracellular" 5 "mitochondrion" 6 "other" 
total1 <- list()
start <- 1
for (i in names(pept[[1]])[1:6]){
  total1[[start]] <- make_corr_list(i, 0.6)
  start <- start + 1
} 


total <- make_corr_list('nucleus', 0.6)

lapply(total1, function(x) write.table(data.frame(x), 'output1.csv'  , append= T, sep=','))






